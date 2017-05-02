DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(128) DEFAULT NULL,
  `email` varchar(128) DEFAULT NULL,
  `pass` varchar(128) DEFAULT NULL,
  `created` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

INSERT INTO `users` VALUES (NULL,'admin','admin@example.com','$2a$10$GE8/7nnNw8rrhqVSyLZBsOANlhAu2JzPmtvcFnw.hvhQ1H4smKtP.',NULL);