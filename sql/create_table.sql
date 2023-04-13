CREATE TABLE concurrent_access.auth_user (
	user_id INT NOT NULL AUTO_INCREMENT,
	user_account VARCHAR(32) UNIQUE,
	user_name VARCHAR(128),
	user_password VARCHAR(129),
	email VARCHAR(128),
	created_date DATE,
	updated_date DATE,
	last_login_date DATE,
	pwd_updated_date DATE,
	PRIMARY KEY(user_id)
);

CREATE TABLE concurrent_access.account_access (
    user_id   INT,
    sid     VARCHAR(32),
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES auth_user(user_id) ON DELETE CASCADE
);

CREATE INDEX idx_auth_account ON concurrent_access.auth_user(user_account);
CREATE INDEX idx_account_access_user ON concurrent_access.account_access(user_id);