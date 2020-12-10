# 네이버 인기검색 순위
CREATE TABLE search_ranking
(
    id           BIGINT AUTO_INCREMENT PRIMARY KEY,
    group_id     INT      NOT NULL,
    ranking      TINYINT      NOT NULL,
    company      VARCHAR(255) NOT NULL,
    created_date DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE INDEX uix_group_id_company (group_id, company),
    INDEX ix_created_date_company (created_date, company)
);

# 한국거래소 상장기업 정보
CREATE TABLE company_info
(
    code        VARCHAR(20) primary key,
    company     VARCHAR(40),
    last_update DATE,
    INDEX ix_company (company)
);
