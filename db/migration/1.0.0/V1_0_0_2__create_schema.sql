# 네이버 인기검색 순위
CREATE TABLE search_ranking
(
    id           BIGINT AUTO_INCREMENT PRIMARY KEY,
    ranking      TINYINT      NOT NULL,
    company      VARCHAR(255) NOT NULL,
    created_date DATETIME     NULL,
    UNIQUE INDEX uix_created_date_company (created_date, company),
    INDEX ix_company (company)
);

# 한국거래소 상장기업 정보
CREATE TABLE company_info
(
    code        VARCHAR(20) primary key,
    company     VARCHAR(40),
    last_update DATE,
    INDEX ix_company (company)
);
