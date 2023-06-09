package com.webtoon.manamana.util.repository;

import com.querydsl.jpa.impl.JPAQueryFactory;

import com.webtoon.manamana.entity.webtoon.codetable.Genre;

import org.springframework.data.jpa.repository.support.QuerydslRepositorySupport;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public class GenreCodeRepositorySupport extends QuerydslRepositorySupport {


    private final JPAQueryFactory queryFactory;

    public GenreCodeRepositorySupport(JPAQueryFactory queryFactory) {
        super(Genre.class);
        this.queryFactory = queryFactory;

    }

}
