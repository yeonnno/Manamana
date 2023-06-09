package com.webtoon.manamana.auth.dto;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class AccessTokenDTO {

    private String accessToken;

    @Builder
    public AccessTokenDTO(String accessToken) {
        this.accessToken = accessToken;
    }
}
