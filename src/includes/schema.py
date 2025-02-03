import settings

from includes.db import Db

class Schema:

    def CreateDatabase():

        query = f"CREATE DATABASE IF NOT EXISTS {settings.DB_NAME} CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci"

        return Db.ExecuteQuery(query, None, True, True)

    def CreateTables():

        #####################################################################################################
        query = """
			CREATE TABLE IF NOT EXISTS emails (
                email_id VARCHAR(255) PRIMARY KEY NOT NULL,
                sender LONGTEXT NOT NULL,
                bcc_recipients JSON NULL,
                purpose VARCHAR(255) NOT NULL,
                subject LONGTEXT DEFAULT NULL,
                message LONGTEXT DEFAULT NULL,
                reply_to JSON DEFAULT NULL,
                cc_recipients JSON NULL,
                delivered BOOLEAN DEFAULT 0,
                date DATETIME NOT NULL
            ) ENGINE=INNODB;
		"""

        if not Db.ExecuteQuery(query, None, True):
            return False

        Db.ExecuteQuery("ALTER TABLE emails ADD INDEX email_id (email_id);", None, True)
        Db.ExecuteQuery("ALTER TABLE emails ADD INDEX sender (sender);", None, True)
        Db.ExecuteQuery("ALTER TABLE emails ADD INDEX purpose (purpose);", None, True)
        Db.ExecuteQuery("ALTER TABLE emails ADD INDEX subject (subject);", None, True)
        Db.ExecuteQuery("ALTER TABLE emails ADD INDEX delivered (delivered);", None, True)
        Db.ExecuteQuery("ALTER TABLE emails ADD INDEX date (date);", None, True)
        #####################################################################################################

        #####################################################################################################
        query = """
			CREATE TABLE IF NOT EXISTS teams (
                teams_id VARCHAR(255) PRIMARY KEY NOT NULL,
                channel LONGTEXT NOT NULL,
                purpose VARCHAR(255) NOT NULL,
                subject LONGTEXT DEFAULT NULL,
                message LONGTEXT DEFAULT NULL,
                delivered BOOLEAN DEFAULT 0,
                date DATETIME NOT NULL
            ) ENGINE=INNODB;
		"""

        if not Db.ExecuteQuery(query, None, True):
            return False

        Db.ExecuteQuery("ALTER TABLE teams ADD INDEX teams_id (teams_id);", None, True)
        Db.ExecuteQuery("ALTER TABLE teams ADD INDEX channel (channel);", None, True)
        Db.ExecuteQuery("ALTER TABLE teams ADD INDEX purpose (purpose);", None, True)
        Db.ExecuteQuery("ALTER TABLE teams ADD INDEX subject (subject);", None, True)
        Db.ExecuteQuery("ALTER TABLE teams ADD INDEX delivered (delivered);", None, True)
        Db.ExecuteQuery("ALTER TABLE teams ADD INDEX date (date);", None, True)
        #####################################################################################################

        #####################################################################################################
        query = """
			CREATE TABLE IF NOT EXISTS batsignal (
                batsignal_id VARCHAR(255) PRIMARY KEY NOT NULL,
                sender LONGTEXT NOT NULL,
                created_by VARCHAR(255) DEFAULT NULL,
                user_id VARCHAR(255) DEFAULT NULL,
                purpose VARCHAR(255) NOT NULL,
                subject LONGTEXT DEFAULT NULL,
                content LONGTEXT DEFAULT NULL,
                broadcast BOOLEAN DEFAULT 0,
                date DATETIME NOT NULL
            ) ENGINE=INNODB;
		"""

        if not Db.ExecuteQuery(query, None, True):
            return False

        Db.ExecuteQuery("ALTER TABLE batsignal ADD INDEX batsignal_id (batsignal_id);", None, True)
        Db.ExecuteQuery("ALTER TABLE batsignal ADD INDEX sender (sender);", None, True)
        Db.ExecuteQuery("ALTER TABLE batsignal ADD INDEX created_by (created_by);", None, True)
        Db.ExecuteQuery("ALTER TABLE batsignal ADD INDEX user_id (user_id);", None, True)
        Db.ExecuteQuery("ALTER TABLE batsignal ADD INDEX subject (subject);", None, True)
        Db.ExecuteQuery("ALTER TABLE batsignal ADD INDEX content (content);", None, True)
        Db.ExecuteQuery("ALTER TABLE batsignal ADD INDEX broadcast (broadcast);", None, True)
        Db.ExecuteQuery("ALTER TABLE batsignal ADD INDEX date (date);", None, True)
        #####################################################################################################

        return True