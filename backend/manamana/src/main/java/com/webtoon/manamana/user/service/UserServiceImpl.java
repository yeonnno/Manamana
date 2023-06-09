package com.webtoon.manamana.user.service;

import com.amazonaws.services.s3.AmazonS3Client;
import com.amazonaws.services.s3.model.CannedAccessControlList;
import com.amazonaws.services.s3.model.ObjectMetadata;
import com.amazonaws.services.s3.model.PutObjectRequest;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.webtoon.manamana.config.aws.AwsDirectoryName;
import com.webtoon.manamana.config.redis.RedisProperty;
import com.webtoon.manamana.config.redis.RedisUtil;
import com.webtoon.manamana.config.response.exception.CustomException;
import com.webtoon.manamana.config.response.exception.CustomExceptionStatus;
import com.webtoon.manamana.entity.user.*;
import com.webtoon.manamana.entity.webtoon.Comment;
import com.webtoon.manamana.entity.webtoon.Webtoon;
import com.webtoon.manamana.entity.webtoon.WebtoonGenre;
import com.webtoon.manamana.entity.webtoon.codetable.Genre;
import com.webtoon.manamana.user.dto.request.UserUpdateRequestDTO;
import com.webtoon.manamana.user.dto.response.GenreResponseDTO;
import com.webtoon.manamana.user.dto.response.UserCommentResponseDTO;
import com.webtoon.manamana.user.dto.response.UserResponseDTO;
import com.webtoon.manamana.user.dto.response.WebtoonInfoDTO;
import com.webtoon.manamana.user.repository.user.*;
import com.webtoon.manamana.util.repository.GenreCodeRepository;
import com.webtoon.manamana.webtoon.repository.comment.CommentRepository;
import com.webtoon.manamana.webtoon.repository.comment.CommentRepositorySupport;
import com.webtoon.manamana.webtoon.repository.webtoon.WebtoonGenreRepository;
import com.webtoon.manamana.webtoon.repository.webtoon.WebtoonRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.jetbrains.annotations.NotNull;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import java.io.IOException;
import java.io.InputStream;
import java.util.*;
import java.util.stream.Collectors;

import static com.webtoon.manamana.config.response.exception.CustomExceptionStatus.*;
import static com.webtoon.manamana.config.response.exception.CustomExceptionStatus.NOT_FOUNT_USER;

@Slf4j
@RequiredArgsConstructor
@Service
public class UserServiceImpl implements UserService{

    private final UserRepository userRepository;
    private final UserRepositorySupport userRepositorySupport;
    private final UserWebtoonRepository userWebtoonRepository;
    private final UserWebtoonRepositorySupport userWebtoonRepositorySupport;
    private final CommentRepository commentRepository;
    private final CommentRepositorySupport commentRepositorySupport;
    private final UserGenreRepository userGenreRepository;
    private final GenreCodeRepository genreCodeRepository;
    private final WebtoonRepository webtoonRepository;
    private final WebtoonGenreRepository webtoonGenreRepository;
    private final PreferGenreRepository preferGenreRepository;
    private final PreferGenreRepositorySupport preferGenreRepositorySupport;

    //aws 업로드
    private final AmazonS3Client amazonS3Client;

    //aws 변수.
    private final AwsDirectoryName awsDirectoryName;
    //레디스
    private final RedisUtil redisUtil;

    //레디스 설정
    private final RedisProperty redisProperty;


    //TODO : jwt로 받은 유저ID와 pathvariable로 받은 유저ID가 같은지 처리하는 로직 필요. - 별도의 메서드로 만들어서 공통처리하도록.



    /*회원 정보 조회*/
    @Transactional(readOnly = true)
    @Override
    public UserResponseDTO getUser(Long userId) {

        //유저 조회
        User user = userCheck(userId);

        //좋아요 수 조회
        Long userWebtoonLikeCount = userWebtoonRepositorySupport.findUserWebtoonLikeCount(user);

        //평가한 웹툰 수 조회
        Long userWebtoonScoreCount = userWebtoonRepositorySupport.findUserWebtoonScoreCount(user);


        return UserResponseDTO.createDTO(user,userWebtoonLikeCount,userWebtoonScoreCount);
    }

    /*회원 정보 수정*/
    @Transactional
    @Override
    public void updateUser(long userId, UserUpdateRequestDTO userUpdateRequestDTO, MultipartFile file) {

        //유저 조회
        User user = userCheck(userId);

        String updateFilePath = "";

        //파일 저장 후 파일 경로 반환 - 없으면 null;
        updateFilePath = saveFile(userId, file);

        //DTO에 파일 경로 저장
        userUpdateRequestDTO.setUserImage(updateFilePath);


        //유저 업데이트
        user.updateUser(userUpdateRequestDTO);

    }


    /*회원 탈퇴*/
    @Transactional
    @Override
    public void removeUser(long userId) {
        //유저 조회
        User user = userCheck(userId);

        //유저 삭제
        user.removeUser();
    }

    /*작성한 댓글 조회*/
    @Transactional(readOnly = true)
    @Override
    public List<UserCommentResponseDTO> getUserCommentAll(long userId) {

        //유저 조회
        User user = userCheck(userId);
        
        //댓글 조회
        List<Comment> commentList = commentRepositorySupport.findByUserCommentAll(user);

        //response DTO로 변환.
        List<UserCommentResponseDTO> userCommentResponseDTOS = commentList.stream()
                .map(UserCommentResponseDTO::createDTO)
                .collect(Collectors.toList());

        return userCommentResponseDTOS;
    }

    /*관심 웹툰 조회 - 요일 별 조회(0이면 전체 조회.).*/
    @Transactional(readOnly = true)
    @Override
    public List<WebtoonInfoDTO> getUserWebtoonAll(long userId, Integer dayId) {
        //유저 조회
        User user = userCheck(userId);

        //관심 웹툰 조회
        List<UserWebtoon> userWebtoons = userWebtoonRepositorySupport.findUserWebtoonLikeAll(user, dayId);

        //

        //response DTO 변환
        List<WebtoonInfoDTO> webtoonInfoDTOS = userWebtoons.stream()
                .map(WebtoonInfoDTO::createDTO)
                .collect(Collectors.toList());

        return webtoonInfoDTOS;
    }

    /*관심 웹툰 삭제*/
    @Transactional
    @Override
    public void deleteUserWebtoon(long userId,List<Long> webtoonIds) {

        //유저 조회
        User user = userCheck(userId);

        //관심 웹툰 조회
        webtoonIds.forEach(id -> {
            //해당 웹툰이 있는지 조회.
            Webtoon webtoon = webtoonRepository.findByIdAndIsDeletedFalse(id)
                    .orElseThrow(() -> new CustomException(NOT_FOUNT_WEBTOON));

            UserWebtoon userWebtoon = userWebtoonRepositorySupport.findUserWetboonLikedByUserAndWebtoon(user,webtoon)
                    .orElseThrow(() -> new CustomException(NOT_FOUND_USER_WEBTOON));

            userWebtoon.removeUserWebtoon();

            // TODO: 2023-04-05 다른 테스트를 위해 주석처리.
            /*
            //레디스에서 저장중이던 sse 객체 삭제.
            Map<Long, SseEmitter> sseMap = redisUtil.getData(redisProperty.getSseKey(), id);

            //값이 없으면 예외
            if(sseMap == null){
                throw new CustomException(CustomExceptionStatus.NOT_FOUND_NOTIFICATION);
            }
            //값이 있지만 해당 유저의 객체가 없을때,
            else if(!sseMap.containsKey(userId)){
                throw new CustomException(CustomExceptionStatus.NOT_FOUND_NOTIFICATION);
            }
            //다 존재하면 삭제.
            else{
                sseMap.remove(userId);
                redisUtil.setData(redisProperty.getSseKey(),id,sseMap);
            }
            */

        });

    }


    /*선호 장르 선택*/
    @Transactional
    @Override
    public void selectLikeGenre(long userId,List<Integer> genreIds) {
        //유저 조회
        User user = userCheck(userId);

        genreIds.forEach(id -> {

            /*유저 장르 연결테이블에 가중치 추가.*/

            //선택된 장르들을 하나씩 조회.
            Genre genre = genreCodeRepository.findById(id)
                    .orElseThrow(() -> new CustomException(NOT_FOUNT_GENRE));


            Optional<UserGenre> userGenreOptional = userGenreRepository.findById(UserGenreId.createUserGenreId(user.getId(), genre.getId()));

            //유저 - 장르가 있으면
            if(userGenreOptional.isPresent()){
                UserGenre userGenre = userGenreOptional.get();

                //유저가 이전에 선택했는지 확인
                Optional<PreferGenre> selectGenreOne = preferGenreRepositorySupport.findSelectGenreOne(user, userGenre.getUserGenreId().getGenreId());

                //장르를 이전에 한번이라도 선택했었다면,
                if(selectGenreOne.isPresent()){
                    userGenre.updateUserGenre(10);
                }
                //장르를 선택한적 없다면,
                else{
                    //장르를 직접 선택한적은 없지만, 웹툰, 관심등록을 통해 간접적으로 생성했기 때문에, 50점을 추가하는 식으로
                    userGenre.updateUserGenre(50);
                }
            }
            //유저 - 장르가 없으면 - 새로 생성함.
            else{
                //유저가 이전에 선택을 한 적이 없으면,유저가 이전에 선택한 선호장르 목록을 확인할 필요 없이 생성하면 됨.
                //만약 이전에 선호장르에서 선택했으면 무조건 유저-장르 테이블도 생성했을것이므로 그냥 생성하면 됨.
                UserGenre newUserGenre = UserGenre.createUserGenre(user, genre);
                userGenreRepository.save(newUserGenre);
            }

        });
        /*선택한 값 업데이트.*/
        //모든 선택장르 가져오기
        List<PreferGenre> selectGenres = preferGenreRepositorySupport.findSelectGenreAll(user);

        //모든 선택된 장르 취소 상태로 만들기
        selectGenres.forEach(selectGenre -> {
            selectGenre.updatePreferGenre(true);
        });

        //id 값으로 조회 하면서 확인.
        genreIds.forEach(genreId -> {

            Optional<PreferGenre> preferGenreOptional = preferGenreRepositorySupport.findSelectGenreOne(user, genreId);

            if(preferGenreOptional.isPresent()){
                PreferGenre preferGenre = preferGenreOptional.get();
                preferGenre.updatePreferGenre(false);

            }
            //값이 없으면 새로 추가.
            else{
                preferGenreRepository.save(PreferGenre.createPreferGenre(user,genreId));
            }

        });
    }

    /*선호했던 장르 조회*/
    @Override
    public GenreResponseDTO findSelectLikeGenre(long userId) {

        //유저 조회
        User user = userRepository.findByIdAndIsDeletedFalse(userId)
                .orElseThrow(() -> new CustomException(NOT_FOUNT_USER));

        //유저가 선택한 장르 조회
        List<PreferGenre> selectGenre = preferGenreRepositorySupport.findSelectGenre(user);

        //DTO 변환.
        GenreResponseDTO genreResponseDTO = GenreResponseDTO.createDTO(selectGenre);

        return genreResponseDTO;
    }


    /*선호 웹툰 선택*/
    @Transactional
    @Override
    public void selectLikeWebtoon(long userId,List<Long> webtoonIds) {

        //유저 조회
        User user = userCheck(userId);

        webtoonIds.forEach(id -> {
            //해당 웹툰 조회
            Webtoon webtoon = webtoonRepository.findByIdAndIsDeletedFalse(id)
                    .orElseThrow(() -> new CustomException(NOT_FOUNT_WEBTOON));

            List<WebtoonGenre> webtoonGenres = webtoonGenreRepository.findByWebtoonId(webtoon.getId());

            webtoonGenres.forEach(webtoonGenre ->
                userGenreRepository.findById(UserGenreId.createUserGenreId(user.getId(), webtoonGenre.getGenre().getId()))
                        .ifPresentOrElse(
                                //장르가 있으면 +2
                                userGenre -> userGenre.updateUserWebtoonGenre(),
                                //입력한적 없으면 5점으로 생성
                                () -> {
                                    UserGenre userGenre = UserGenre.createUserWebtoonGenre(user, webtoonGenre.getGenre());
                                    userGenreRepository.save(userGenre);
                                })
            );
        });
    }

    /*유틸 메서드*/
    //유저 조회하는 메서드
    public User userCheck(long userId) {

        User user = userRepository.findByIdAndIsDeletedFalse(userId)
                .orElseThrow(() -> new CustomException(NOT_FOUNT_USER));
        return user;
    }

    /*S3 파일 저장.*/
    public String saveFile(long userId, MultipartFile file) {

        if(file == null) return null;

        String storageFileUrl;

        //저장에 필요한 메타데이터
        ObjectMetadata objectMetadata = new ObjectMetadata();
        objectMetadata.setContentType(file.getContentType());
        objectMetadata.setContentLength(file.getSize());

        //유저가 업로드한 파일의 이름
        String originFileName = file.getOriginalFilename();

        //만약 null이라면 확장자 명을 png로 해서 저장 - 이미지이므로.
        String ext = "png";

        if(originFileName != null){
            //확장자 추출
            int index = originFileName.lastIndexOf(".");
            ext = originFileName.substring(index+1);
        }


        //저장할 이름
        String storeFileName = UUID.randomUUID().toString() + "." + ext;

        //파일 저장위치
        String key = awsDirectoryName.getProfileImage() + userId + "/" + storeFileName;

        try (InputStream inputStream = file.getInputStream()) {
            amazonS3Client.putObject(new PutObjectRequest(awsDirectoryName.getBucket(), key, inputStream, objectMetadata)
                    .withCannedAcl(CannedAccessControlList.PublicRead));
        }
        catch(IOException e){

            throw new CustomException(FILE_SAVE_FAIL);
        }

        storageFileUrl = amazonS3Client.getUrl(awsDirectoryName.getBucket(),key).toString();

        return storageFileUrl;
    }
}
