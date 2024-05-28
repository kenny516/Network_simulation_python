CREATE DATABASE networkSimulation;
USE networkSimulation;

CREATE TABLE server
(
    id_server  INT PRIMARY KEY auto_increment,
    address_IP VARCHAR(50),
    status     boolean
);

CREATE TABLE DNS
(
    id_dns      INT PRIMARY KEY auto_increment,
    id_server   INT NOT NULL,
    domain_name VARCHAR(255),
    FOREIGN KEY (id_server) REFERENCES server (id_server)
);

CREATE TABLE path_server
(
    id_path     INT PRIMARY KEY auto_increment,
    id_server_1 INT NOT NULL,
    id_server_2 INT NOT NULL,
    time        INT,
    FOREIGN KEY (id_server_1) REFERENCES server (id_server),
    FOREIGN KEY (id_server_2) REFERENCES server (id_server)

);

-- Exemples de données pour la table server
INSERT INTO server (address_IP, status) VALUES
('192.168.0.1', true),
('10.0.0.5', false),
('172.16.0.10', true);

-- Exemples de données pour la table DNS
INSERT INTO DNS (id_server, domain_name) VALUES
(1, 'facebook.com'),
(2, 'test.org'),
(3, 'mywebsite.net');

-- Exemples de données pour la table path_server
INSERT INTO path_server (id_server_1, id_server_2, time) VALUES
(1, 2, 10),
(2, 3, 15),
(3, 1, 20);
