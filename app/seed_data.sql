-- Real hockey teams
INSERT INTO team (name) VALUES
('Montreal Canadiens'),
('Toronto Maple Leafs'),
('Boston Bruins'),
('New York Rangers'),
('Chicago Blackhawks'),
('Detroit Red Wings'),
('Edmonton Oilers'),
('Pittsburgh Penguins');

-- Real tournaments
INSERT INTO tournament (name) VALUES
('Stanley Cup Playoffs 2025'),
('NHL Winter Classic 2026');

-- Past matches (using team IDs 1-8)
-- Tournament 1: Stanley Cup Playoffs 2025
INSERT INTO match (tournament_id, home_team_id, away_team_id, home_score, away_score, played_at) VALUES
(1, 1, 2, 4, 3, '2025-10-01 19:00:00'),
(1, 3, 4, 2, 5, '2025-10-05 20:00:00'),
(1, 5, 6, 3, 2, '2025-10-10 18:30:00'),
(1, 7, 8, 1, 4, '2025-10-15 21:00:00'),
(1, 2, 3, 5, 2, '2025-10-20 19:30:00'),
(1, 4, 1, 3, 3, '2025-10-25 20:00:00');

-- Tournament 2: NHL Winter Classic 2026
INSERT INTO match (tournament_id, home_team_id, away_team_id, home_score, away_score, played_at) VALUES
(2, 6, 5, 2, 1, '2025-10-02 15:00:00'),
(2, 8, 7, 4, 4, '2025-10-08 19:00:00'),
(2, 1, 3, 3, 5, '2025-10-12 20:30:00'),
(2, 2, 4, 2, 3, '2025-10-18 18:00:00'),
(2, 5, 8, 1, 2, '2025-10-22 21:00:00'),
(2, 6, 7, 4, 1, '2025-10-26 19:30:00');

-- Future matches (no scores yet)
-- Tournament 1: Stanley Cup Playoffs 2025
INSERT INTO match (tournament_id, home_team_id, away_team_id, home_score, away_score, played_at) VALUES
(1, 1, 5, NULL, NULL, '2026-11-15 19:00:00'),
(1, 2, 6, NULL, NULL, '2026-11-20 20:00:00'),
(1, 3, 7, NULL, NULL, '2026-11-25 18:30:00'),
(1, 4, 8, NULL, NULL, '2026-12-01 21:00:00');

-- Tournament 2: NHL Winter Classic 2026
INSERT INTO match (tournament_id, home_team_id, away_team_id, home_score, away_score, played_at) VALUES
(2, 8, 1, NULL, NULL, '2026-11-18 19:00:00'),
(2, 7, 2, NULL, NULL, '2026-11-22 20:30:00'),
(2, 6, 3, NULL, NULL, '2026-11-28 18:00:00'),
(2, 5, 4, NULL, NULL, '2026-12-05 19:30:00');
