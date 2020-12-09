# create search_rank
CREATE TABLE search_rank (
    id           BIGINT AUTO_INCREMENT PRIMARY KEY,
    rank         TINYINT      NOT NULL,
    company      VARCHAR(255) NOT NULL,
    created_date DATETIME     NULL,
    UNIQUE INDEX uix_created_date_company (created_date, company),
    INDEX ix_company (company)
);
