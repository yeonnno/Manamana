package com.webtoon.manamana.user.controller;

import com.nimbusds.jose.shaded.json.JSONArray;
import com.nimbusds.jose.shaded.json.JSONObject;
import com.nimbusds.jose.shaded.json.parser.JSONParser;
import com.webtoon.manamana.config.response.CommonResponse;
import com.webtoon.manamana.config.response.CustomSuccessStatus;
import com.webtoon.manamana.config.response.DataResponse;
import com.webtoon.manamana.config.response.ResponseService;
import com.webtoon.manamana.user.dto.request.GenreRequestDTO;
import com.webtoon.manamana.user.dto.request.WebtoonRequestDTO;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

@Tag(name = "회원 상호작용 기능", description = "회원 상호작용 관련 기능 관련 API 모음")
@Slf4j
@RequiredArgsConstructor
@RestController
@RequestMapping("/users")
public class UserInteractionController {

    private final ResponseService responseService;

    /*회원이 작성한 댓글 조회*/
    @Tag(name = "회원 상호작용 기능")
    @Operation(summary = "작성한 댓글 조회", description =  "작성한 댓글 조회 기능")
    @ApiResponses({
            @ApiResponse(responseCode = "200",description = "API 정상 동작"),
            @ApiResponse(responseCode = "400",description = "API 에러"),
    })
    @GetMapping("/{user-id}/comments")
    public DataResponse<Object> findUserComment(
            @PathVariable("user-id") long userId) throws Exception{

        String temp1 ="{\n" +
                "\t\t\t\"id\": 1,\n" +
                "\t\t\t\"content\": \"이게 완달....? 가슴이 웅장해진다...\", \n" +
                "\t\t\t\"createTime\": \"2023-03-13 11:22:33\", \n" +
                "\t\t\t\"webtoons\": {\n" +
                "\t\t\t\t\"id\": 1, \n" +
                "\t\t\t\t\"name\": \"호랑이형님\",\n" +
                "\t\t\t\t\"imagePath\": \"https://image-comic.pstatic.net/webtoon/650305/thumbnail/thumbnail_IMAG21_3631086797392995425.jpg\"\n" +
                "\t\t\t}\n" +
                "\t\t}";

        String temp2 ="{\n" +
                "\t\t\t\"id\": 3,\n" +
                "\t\t\t\"content\": \"재밌어요ㅠㅠ\", \n" +
                "\t\t\t\"createTime\": \"2023-03-12 11:22:33\", \n" +
                "\t\t\t\"webtoons\": {\n" +
                "\t\t\t\t\"id\": 2, \n" +
                "\t\t\t\t\"name\": \"내일\",\n" +
                "\t\t\t\t\"imagePath\": \"https://image-comic.pstatic.net/webtoon/695796/thumbnail/thumbnail_IMAG21_332bb25b-c77d-477f-9979-5a8607ebd7a5.jpg\"\n" +
                "\t\t\t}\n" +
                "\t\t}";

        JSONArray jsonArray = new JSONArray();
        JSONParser jsonParser = new JSONParser();

        JSONObject jsonObj1 = (JSONObject) jsonParser.parse(temp1);
        JSONObject jsonObj2 = (JSONObject) jsonParser.parse(temp2);

        jsonArray.add(jsonObj1);
        jsonArray.add(jsonObj2);

        return responseService.getDataResponse(jsonArray,CustomSuccessStatus.RESPONSE_SUCCESS);
    }

    /*관심 웹툰 조회*/
    @Tag(name = "회원 상호작용 기능")
    @Operation(summary = "관심 웹툰 조회", description =  "관심 웹툰 조회 기능")
    @ApiResponses({
            @ApiResponse(responseCode = "200",description = "API 정상 동작"),
            @ApiResponse(responseCode = "400",description = "API 에러"),
    })
    @GetMapping("/{user-id}/webtoons")
    public DataResponse<Object>  findUserWebtoon(
            @PathVariable("user-id") long userId) throws Exception{

        String temp1 = "{\n" +
                "\t\t\t\t\"id\": 1,\n" +
                "\t\t\t\t\"name\": \"호랑이형님\",\n" +
                "\t\t\t\t\"authors\": [\n" +
                "\t\t\t\t\t{\n" +
                "\t\t\t\t\t\t\"id\": 1, \n" +
                "\t\t\t\t\t\t\"name\": \"이상규\"\n" +
                "\t\t\t\t\t}\n" +
                "\t\t\t\t],\n" +
                "\t\t\t\t\"imagePath\": \"https://image-comic.pstatic.net/webtoon/650305/thumbnail/thumbnail_IMAG21_3631086797392995425.jpg\",\n" +
                "\t\t\t\t\"status\": {\n" +
                "\t\t\t\t\t\"id\": 1,\n" +
                "\t\t\t\t\t\"status\": \"연재중\"\n" +
                "\t\t\t\t}\n" +
                "\t\t\t}";
        String temp2 = "{\n" +
                "\t\t\t\t\"id\": 2,\n" +
                "\t\t\t\t\"name\": \"내일\",\n" +
                "\t\t\t\t\"authors\": [\n" +
                "\t\t\t\t\t{\n" +
                "\t\t\t\t\t\t\"id\": 3, \n" +
                "\t\t\t\t\t\t\"name\": \"라마\"\n" +
                "\t\t\t\t\t}\n" +
                "\t\t\t\t],\n" +
                "\t\t\t\t\"imagePath\": \"https://image-comic.pstatic.net/webtoon/695796/thumbnail/thumbnail_IMAG21_332bb25b-c77d-477f-9979-5a8607ebd7a5.jpg\",\n" +
                "\t\t\t\t\"status\": {\n" +
                "\t\t\t\t\t\"id\": 2,\n" +
                "\t\t\t\t\t\"status\": \"완결\"\n" +
                "\t\t\t\t}\n" +
                "\t\t\t}";

        JSONArray jsonArray = new JSONArray();
        JSONParser jsonParser = new JSONParser();

        JSONObject jsonObj1 = (JSONObject) jsonParser.parse(temp1);
        JSONObject jsonObj2 = (JSONObject) jsonParser.parse(temp2);

        jsonArray.add(jsonObj1);
        jsonArray.add(jsonObj2);

        return responseService.getDataResponse(jsonArray, CustomSuccessStatus.RESPONSE_SUCCESS);

    }

    /*관심 웹툰 삭제*/
    @Tag(name = "회원 상호작용 기능")
    @Operation(summary = "관심 웹툰 삭제", description =  "관심 웹툰 삭제 기능")
    @ApiResponses({
            @ApiResponse(responseCode = "200",description = "API 정상 동작"),
            @ApiResponse(responseCode = "400",description = "API 에러"),
    })
    @DeleteMapping("/{user-id}/webtoons")
    public CommonResponse deleteUserWebtoon(
            @PathVariable("user-id") long userId
    ){

        return responseService.getSuccessResponse();
    }

    /*선호 장르 선택*/
    @Tag(name = "회원 상호작용 기능")
    @Operation(summary = "선호 장르 선택", description =  "선호 장르 선택 기능")
    @ApiResponses({
            @ApiResponse(responseCode = "200",description = "API 정상 동작"),
            @ApiResponse(responseCode = "400",description = "API 에러"),
    })
    @PostMapping("/{user-id}/genre/select")
    public CommonResponse userSelectGenre(
            @PathVariable("user-id") long userId,
            @RequestBody GenreRequestDTO genreRequestDTO){

        log.info(genreRequestDTO.getId().toString());
        return responseService.getSuccessResponse();
    }


    /*선호 웹툰 선택*/
    @Tag(name = "회원 상호작용 기능")
    @Operation(summary = "선호 웹툰 선택", description =  "선호 웹툰 선택 기능")
    @ApiResponses({
            @ApiResponse(responseCode = "200",description = "API 정상 동작"),
            @ApiResponse(responseCode = "400",description = "API 에러"),
    })
    @PostMapping("/{user-id}/webtoon/select")
    public CommonResponse userSelectWebtoon(
            @PathVariable("user-id") long userId,
            @RequestBody WebtoonRequestDTO webtoonRequestDTO){


        log.info(webtoonRequestDTO.getId().toString());

        return responseService.getSuccessResponse();
    }
}