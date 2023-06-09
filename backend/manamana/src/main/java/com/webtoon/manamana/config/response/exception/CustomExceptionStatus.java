package com.webtoon.manamana.config.response.exception;

import lombok.*;

@Getter
@RequiredArgsConstructor
public enum CustomExceptionStatus {

    /*common error*/
    REQUEST_ERROR(false, 400, "요청을 확인해주세요."),
    //EMPTY_JWT(false, 401, "JWT를 입력해주세요."),
    INVALID_JWT(false, 401, "유효하지 않은 JWT입니다."),
    //INVALID_USER_JWT(false,403,"권한이 없는 유저의 접근입니다."),
    //NOT_AUTHENTICATED_ACCOUNT(false, 403, "로그인이 필요합니다."),

    NOT_FOUND_REFRESH_TOKEN(false, 400, "리프레시 토큰이 없습니다."),

    NOT_INVALID_REFRESH_TOKEN(false, 401, "유효하지 않은 리프레시 토큰입니다."),


    //
    REFRESH_TOKEN_RENEWAL(false, 401, "리프레시 토큰 재발급 필요."),

    /*인가*/
    HAVE_NO_AUTHORITY(false, 403, "권한이 없습니다."),

    /*인증 - 토큰 관련*/
    TOKEN_INVALID(false,401,"유효하지 않은 토큰입니다."),
    TOKEN_EXPIRE(false,401,"토큰이 만료되었습니다."),

    TOKEN_UNSUPPORTED(false,401,"지원하지 않는 토큰입니다."),
    TOKEN_ILLEGAL(false,401,"잘못된 토큰입니다."),
    TOKEN_NOT_FOUND(false, 401, "토큰이 없습니다."),



    REQUEST_QUERY_ERROR(false, 400, "잘못된 쿼리 요청입니다."),

    /*association user*/
    NOT_FOUNT_USER(false, 401,"해당하는 유저정보가 없습니다."),

    /*유저 웹툰 연관*/
    NOT_FOUND_USER_WEBTOON(false,400,"관심웹툰이 아니거나 이미 삭제한 관심웹툰입니다."),

    /*유저 장르 연관*/
    NOT_FOUNT_GENRE(false, 400, "해당하는 장르가 없습니다."),

    /*웹툰 관련*/
    NOT_FOUNT_WEBTOON(false, 400, "해당하는 웹툰이 없습니다."),
    NOT_FOUNT_WEBTOON_ADDITION(false, 400,"잘못된 접근입니다."),

    /*웹툰 제공자 관련*/
    BAD_PROVIDER_REQUEST(false, 400, "잘못된 웹툰 제공자 요청입니다."),

    /*댓글 관련*/
    NOT_FOUNT_COMMENT(false, 400, "해당하는 댓글을 찾을 수 없습니다."),
    BAD_COMMENT_REQUEST(false,400,"잘못된 댓글 접근입니다."),

    /*신고 관련*/
    ALREADY_REPORT_COMMENT(false, 400,"이미 신고한 댓글입니다."),

    /*관심 등록 관련*/
    ALREADY_LIKE_WEBTOON(false, 400, "이미 관심등록 된 웹툰입니다."),
    NOT_FOUND_SCORE(false, 400, "이전에 평가한 점수가 없습니다."),

    /*S3관련*/
    FILE_SAVE_FAIL(false, 400, "파일 저장에 실패했습니다."),

    /*login provider 관련*/
    NOT_FOUNT_PROVIDER(false, 400, "해당하는 로그인 제공자를 찾을 수 없습니다."),

    /*알림 기능.*/
    NOT_FOUND_NOTIFICATION(false, 400, "해당하는 알림을 찾을 수 없습니다."),
    FAIL_CONNECT_SSE(false, 400, "알림등록에 실패했습니다."),
    ALREADY_NOTIFICATION(false, 400, "이미 알림이 등록되어있습니다."),

    /*추천관련*/
    NOT_FOUND_RECOMMEND_WEBTOON(false,400,"장르 추천 웹툰이 없습니다"),




    /*Object Mapper 관련에러*/
    TRANSFER_FAIL(false, 400, "데이터 변환에 실패했습니다."),

    ;
    private final boolean isSuccess;

    private final int code;

    private final String message;
}
