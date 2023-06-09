package com.webtoon.manamana.user.repository.user;

import com.nimbusds.jose.util.IntegerUtils;
import com.querydsl.core.types.dsl.BooleanExpression;
import com.querydsl.core.types.dsl.Wildcard;
import com.querydsl.core.util.StringUtils;
import com.querydsl.jpa.impl.JPAQueryFactory;
import com.webtoon.manamana.entity.user.QUser;
import com.webtoon.manamana.entity.user.QUserWebtoon;
import com.webtoon.manamana.entity.user.User;
import com.webtoon.manamana.entity.user.UserWebtoon;
import com.webtoon.manamana.entity.webtoon.QWebtoon;
import com.webtoon.manamana.entity.webtoon.QWebtoonDay;
import com.webtoon.manamana.entity.webtoon.Webtoon;
import com.webtoon.manamana.entity.webtoon.codetable.QSerialStatus;
import lombok.RequiredArgsConstructor;
import org.springframework.data.jpa.repository.support.QuerydslRepositorySupport;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

import static com.webtoon.manamana.entity.user.QUserWebtoon.userWebtoon;

@Repository
public class UserWebtoonRepositorySupport extends QuerydslRepositorySupport {

    private final JPAQueryFactory queryFactory;

    public UserWebtoonRepositorySupport(JPAQueryFactory queryFactory) {
        super(UserWebtoon.class);
        this.queryFactory = queryFactory;
    }


    //유저 관심등록 테이블 조회 - 관심등록 상관 없이 조회.
    public Optional<UserWebtoon> findUserWebtoonByUserAndWebtoon(long userId, long webtoonId){

        QUserWebtoon userWebtoon = QUserWebtoon.userWebtoon;

        return Optional.ofNullable(
                queryFactory
                        .selectFrom(userWebtoon)
                        .where(userWebtoon.isDeleted.eq(false), userWebtoon.user.id.eq(userId),userWebtoon.webtoon.id.eq(webtoonId))
                        .fetchOne()
        );
    }

    // fetchCount()는 deprecated 됨
    /*웹툰 좋아요 한 갯수*/
    public Long findUserWebtoonLikeCount(User user){
        return queryFactory
                .select(Wildcard.count)
                .from(userWebtoon)
                .where(userWebtoon.isDeleted.eq(false)
                        .and(userWebtoon.isLiked.eq(true)
                                .and(userWebtoon.user.eq(user))))
                .fetchOne();
    }

    /*평가한 웹툰 수 - 평가 점수가 0보다 커야됨.*/
    public Long findUserWebtoonScoreCount(User user){

        return queryFactory
                .select(userWebtoon.user.count())
                .from(userWebtoon)
                .where(userWebtoon.isDeleted.eq(false)
                        .and(userWebtoon.score.ne(0)
                                .and(userWebtoon.user.eq(user))))
                .fetchOne();
    }

    /*유저가 관심있어한 웹툰*/
    public List<UserWebtoon> findUserWebtoonLikeAll(User user, Integer dayId){

        return queryFactory
                .selectFrom(userWebtoon)
                .where(
                        userWebtoon.isDeleted.eq(false)
                        .and(userWebtoon.isLiked.eq(true))
                                .and(userWebtoon.user.eq(user)))
                .leftJoin(userWebtoon.webtoon, QWebtoon.webtoon)
                .fetchJoin()
                .where(QWebtoon.webtoon.isDeleted.eq(false))
                .leftJoin(QWebtoon.webtoon.webtoonDays, QWebtoonDay.webtoonDay)
                .fetchJoin()
                .where(eqDayId(dayId))
                .distinct().fetch();
    }

    /*Boolean Expression - null이면 조건문 제외*/
    private BooleanExpression eqDayId(Integer dayId){
        if(dayId == null) return null;

        return QWebtoonDay.webtoonDay.codeId.eq(dayId);
    }

    /*유저가 관심등록했는지 여부 확인.*/
    public Optional<UserWebtoon> findUserWetboonLikedByUserAndWebtoon(User user, Webtoon webtoon){

        QUserWebtoon userWebtoon = QUserWebtoon.userWebtoon;

        return Optional.ofNullable(
                queryFactory
                .selectFrom(userWebtoon)
                .where(userWebtoon.user.eq(user),
                        userWebtoon.webtoon.eq(webtoon),
                        userWebtoon.isDeleted.eq(false),
                        userWebtoon.isLiked.eq(true))
                .fetchOne()
        );
    }

    public List<UserWebtoon> findByUserIdAndIsDeletedFalse(long userId) {

        QUserWebtoon userWebtoon = QUserWebtoon.userWebtoon;

        return queryFactory
                .selectFrom(userWebtoon)
                .where(userWebtoon.user.id.eq(userId)
                        .and(userWebtoon.isDeleted.eq(false)))
                .fetch();
    }

    public List<UserWebtoon> findByWebtoonIdAndIsDeletedFalse(long webtoonId) {

        QUserWebtoon userWebtoon = QUserWebtoon.userWebtoon;

        return queryFactory
                .selectFrom(userWebtoon)
                .where(userWebtoon.webtoon.id.eq(webtoonId)
                        .and(userWebtoon.isDeleted.eq(false)))
                .fetch();
    }

    /* 유저가 관심등록한 웹툰 조회 */
    public List<Long> findLikeWebtoonByUserId(long userId) {

        QUserWebtoon userWebtoon = QUserWebtoon.userWebtoon;

        return queryFactory
                .select(userWebtoon.webtoon.id)
                .from(userWebtoon)
                .where(userWebtoon.user.id.eq(userId)
                        .and(userWebtoon.isLiked.eq(true))
                        .and(userWebtoon.isDeleted.eq(false)))
                .fetch();
    }
}
