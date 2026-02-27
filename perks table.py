CREATE TABLE perks (
    ->     id INT PRIMARY KEY AUTO_INCREMENT,
    ->     perk_name VARCHAR(50),
    ->     value INT,
    ->     game_id VARCHAR(40)
    -> );

#laita tämä ensimmäisen jälkeen muuten ei toimi
MODIFY game_id VARCHAR(40) CHARACTER SET latin1 COLLATE latin1_swedish_ci;
#viimeisenä tämä
ALTER TABLE perks
    -> ADD CONSTRAINT fk_game_id
    -> FOREIGN KEY (game_id) REFERENCES game(id);