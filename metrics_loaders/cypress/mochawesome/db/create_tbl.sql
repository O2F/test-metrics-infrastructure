CREATE TABLE `grafana`.`mochawesome` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `create_datetime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `suites_nr` INT NOT NULL,
  `tests_nr` INT NOT NULL,
  `passes` INT NOT NULL,
  `pending` INT NOT NULL,
  `failures` INT NOT NULL,
  `skipped` INT NOT NULL,
  `duration_ms` INT NOT NULL,
  `pass_percent` DOUBLE NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE = InnoDB;
