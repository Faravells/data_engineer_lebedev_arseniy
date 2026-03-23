CREATE TABLE event (
  event_id INT PRIMARY KEY AUTO_INCREMENT,
  event_name VARCHAR(30) UNIQUE NOT NULL
);

CREATE TABLE log (
  log_id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT,
  event_id INT NOT NULL,
  description VARCHAR(200),
  forum_id INT,
  status VARCHAR(20),
  time DATETIME DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (event_id) REFERENCES event(event_id)
);

INSERT INTO event (event_name)
VALUES
  ('first_visit'),
  ('registration'),
  ('login'),
  ('logout'),
  ('create_topic'),
  ('visit_topic'),
  ('delete_topic'),
  ('write_message');
