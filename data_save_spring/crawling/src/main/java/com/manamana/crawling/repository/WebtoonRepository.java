package com.manamana.crawling.repository;

import com.manamana.crawling.entity.webtoon.Webtoon;
import com.manamana.crawling.entity.webtoon.WebtoonProvider;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface WebtoonRepository extends JpaRepository<Webtoon, Long> {

    Optional<Webtoon> findByWebtoonIdAndProviderId(String webtoonId, WebtoonProvider ProviderId);

    Optional<Webtoon> findByName(String name);

}
