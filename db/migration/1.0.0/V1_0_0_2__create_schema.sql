# 네이버 인기검색 순위
CREATE TABLE search_ranking
(
    id           BIGINT AUTO_INCREMENT PRIMARY KEY,
    group_id     INT          NOT NULL,
    ranking      TINYINT      NOT NULL,
    company      VARCHAR(255) NOT NULL,
    step         TINYINT      NOT NULL,
    created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE INDEX uix_group_id_company (group_id, company),
    INDEX ix_created_date_company (created_at, company)
);

# 한국거래소 상장기업 정보
CREATE TABLE company_info
(
    code        VARCHAR(20) primary key,
    company     VARCHAR(40),
    updated_at DATE,
    INDEX ix_company (company)
);

# 시간외 단일가
CREATE TABLE `after_hours` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `market` varchar(10) NOT NULL COMMENT '코스피 / 코스닥',
  `rank` int(11) NOT NULL COMMENT '순위',
  `name` varchar(100) NOT NULL DEFAULT '' COMMENT '종목',
  `symbolCode` varchar(50) NOT NULL DEFAULT '',
  `code` varchar(50) NOT NULL DEFAULT '',
  `tradePrice` decimal(10,0) NOT NULL COMMENT '시외 체결가',
  `changeRate` decimal(10,0) NOT NULL COMMENT '시외 등락률',
  `accTradeVolume` decimal(10,0) NOT NULL COMMENT '시외 체결량',
  `regularHoursTradePrice` decimal(10,0) NOT NULL COMMENT '정규장 종가',
  `regularHoursChange` varchar(10) NOT NULL DEFAULT '' COMMENT '정규장 등락 구분',
  `regularHoursChangeRate` decimal(10,0) NOT NULL COMMENT '정규장 등락률',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ix_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4;