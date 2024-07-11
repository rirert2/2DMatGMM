-- @block
CREATE TABLE Chips(
    chip_id INT PRIMARY KEY AUTO_INCREMENT,
    material VARCHAR(255) NOT NULL,
    size INT NOT NULL -- mm squared
);

-- @block
INSERT INTO flakes (chip_id, flake_id)
VALUES (
    '1',
    '1'
);

-- @block
INSERT INTO chips (material, size)
VALUES (
    'Wse2',
    '2'
);

-- @block 
SELECT * FROM flakes

WHERE chip_id = 2

ORDER BY chip_id asc;

-- @block
CREATE INDEX material_index ON Chips(material);

-- @block
CREATE TABLE Flakes(
    chip_id INT NOT NULL, -- prefer it this way so it can be read as (1,2)
    flake_id INT,
    FOREIGN KEY (chip_id) REFERENCES Chips(chip_id),
    PRIMARY KEY (chip_id, flake_id)
); 
-- Note that the flake_id WILL NOT AUTO INCREMENT

-- @block
DROP TABLE chips;