USE AI_COOK;

-- ==========================================
-- INGREDIENTI
-- ==========================================
INSERT INTO INGREDIENTI (nome) VALUES
('Spaghetti'),           -- 1
('Guanciale'),           -- 2
('Uova'),                -- 3
('Pecorino Romano'),     -- 4
('Pepe nero'),           -- 5
('Sale'),                -- 6
('Pollo'),               -- 7
('Limone'),              -- 8
('Aglio'),               -- 9
('Rosmarino'),           -- 10
('Olio d\'oliva'),       -- 11
('Farina'),              -- 12
('Burro'),               -- 13
('Zucchero'),            -- 14
('Uova (tuorlo)'),       -- 15
('Latte'),               -- 16
('Vaniglia'),            -- 17
('Zucchero a velo');     -- 18

-- ==========================================
-- RICETTE
-- ==========================================
INSERT INTO RICETTA (idCategoria, nome, descrizione, tempo, difficoltà) VALUES
(1, 'Spaghetti alla Carbonara',   'Il classico primo romano con guanciale e uova',          25, 'Media'),
(2, 'Pollo al Limone',            'Secondo leggero e profumato con pollo e limone fresco',  40, 'Bassa'),
(4, 'Pasta Frolla',               'Base dolce friabile per crostate e biscotti',            60, 'Bassa');

-- ==========================================
-- RICETTE <-> INGREDIENTI
-- ==========================================

-- Carbonara (idRicetta = 1)
INSERT INTO RICETTEINGREDIENTI (idIngrediente, idRicetta, quantità, unita_di_misura) VALUES
(1,  1, 320, 'g'),        -- Spaghetti
(2,  1, 150, 'g'),        -- Guanciale
(3,  1, 4,   'unita'),    -- Uova
(4,  1, 80,  'g'),        -- Pecorino Romano
(5,  1, 1,   'pizzico'),  -- Pepe nero
(6,  1, 1,   'pizzico');  -- Sale

-- Pollo al Limone (idRicetta = 2)
INSERT INTO RICETTEINGREDIENTI (idIngrediente, idRicetta, quantità, unita_di_misura) VALUES
(7,  2, 600, 'g'),        -- Pollo
(8,  2, 2,   'unita'),    -- Limone
(9,  2, 2,   'spicchi'),  -- Aglio
(10, 2, 2,   'rametti'),  -- Rosmarino
(11, 2, 3,   'tbsp'),     -- Olio d'oliva
(6,  2, 1,   'pizzico');  -- Sale

-- Pasta Frolla (idRicetta = 3)
INSERT INTO RICETTEINGREDIENTI (idIngrediente, idRicetta, quantità, unita_di_misura) VALUES
(12, 3, 300, 'g'),        -- Farina
(13, 3, 150, 'g'),        -- Burro
(14, 3, 100, 'g'),        -- Zucchero
(15, 3, 2,   'unita'),    -- Uova (tuorlo)
(17, 3, 1,   'bustina'),  -- Vaniglia
(6,  3, 1,   'pizzico');  -- Sale

-- ==========================================
-- PREPARAZIONE
-- ==========================================

-- Carbonara
INSERT INTO PREPARAZIONE (idRicetta, progressivo, descrizione) VALUES
(1, 1, 'Tagliare il guanciale a cubetti e farlo rosolare in padella senza olio fino a renderlo croccante.'),
(1, 2, 'In una ciotola sbattere le uova con il pecorino grattugiato e una generosa macinata di pepe.'),
(1, 3, 'Cuocere gli spaghetti in abbondante acqua salata e scolarli al dente conservando un po\' di acqua.'),
(1, 4, 'Mantecare gli spaghetti nella padella col guanciale, spegnere il fuoco, aggiungere il composto di uova.'),
(1, 5, 'Mescolare velocemente aggiungendo poca acqua di cottura fino a ottenere una crema liscia. Servire subito.');

-- Pollo al Limone
INSERT INTO PREPARAZIONE (idRicetta, progressivo, descrizione) VALUES
(2, 1, 'Marinare il pollo con succo di limone, aglio schiacciato, rosmarino e olio per almeno 30 minuti.'),
(2, 2, 'Scaldare una padella a fuoco medio-alto e rosolare il pollo su tutti i lati fino a doratura.'),
(2, 3, 'Sfumare con il succo della marinatura e cuocere coperto per 20 minuti a fuoco basso.'),
(2, 4, 'Scoprire e far restringere il sughetto per 5 minuti. Servire con fette di limone fresco.');

-- Pasta Frolla
INSERT INTO PREPARAZIONE (idRicetta, progressivo, descrizione) VALUES
(3, 1, 'Tagliare il burro freddo a cubetti e sabbiarlo con la farina lavorando velocemente con le mani.'),
(3, 2, 'Aggiungere lo zucchero, i tuorli, la vaniglia e il pizzico di sale. Impastare fino a ottenere un panetto.'),
(3, 3, 'Avvolgere il panetto nella pellicola trasparente e riporre in frigorifero per almeno 30 minuti.'),
(3, 4, 'Stendere la frolla su un piano infarinato a circa 5mm di spessore e usarla come desiderato.');