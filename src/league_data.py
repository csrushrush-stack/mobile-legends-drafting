# -*- coding: utf-8 -*-
"""League hero-stat tables for the draft app.

Every row is (hero, picks, wins, losses, bans).
Win/loss derived from the published win rate where the source gave a percentage.
'games' is the tournament game count, verified against the published ban% where possible.
"""

# ---- Asian Games 2026 (Aichi-Nagoya) - 32 games, 15 tracked heroes -------------
AG2026 = dict(id="ag", name="Asian Games 2026", short="AG26", region="International",
              games=32, note="MLBB's debut as an official medal event. Gold: Myanmar.",
              rows=[("Nolan",23,11,12,6),("Hirara",16,12,4,15),("Aulus",16,11,5,16),
                    ("Eudora",16,10,6,7),("Obsidia",15,9,6,6),("Esmeralda",14,7,7,8),
                    ("Atlas",13,8,5,19),("Minotaur",13,8,5,13),("Uranus",13,5,8,12),
                    ("Zhuxin",12,6,6,3),("Gloo",11,7,4,6),("Paquito",11,5,6,13),
                    ("Carmilla",11,3,8,19),("Belerick",9,2,7,4),("Valentina",6,6,0,6)])

# ---- MPL Philippines S18 - 167 games ---------------------------------------
PH18 = dict(id="ph", name="MPL Philippines S18", short="PH", region="Philippines",
            games=167, note="Current MPL PH season. Hirara is the most-picked hero in the league.",
            rows=[("Hirara",122,55,67,38),("Paquito",70,42,28,76),("Belerick",67,36,31,25),
                  ("Eudora",64,32,32,30),("Nolan",62,36,26,34),("Minotaur",56,26,30,20),
                  ("Gatotkaca",54,22,32,12),("Barats",51,29,22,59),("Carmilla",49,22,27,44),
                  ("Aulus",47,26,21,30),("Valentina",46,21,25,34),("Marcel",44,25,19,73),
                  ("Uranus",42,21,21,72),("Claude",41,25,16,8),("Zhuxin",39,22,17,33),
                  ("Obsidia",37,19,18,24),("Selena",36,17,19,63),("Clint",32,23,9,11),
                  ("Hylos",31,15,16,6),("Atlas",30,19,11,132),("Rafaela",29,19,10,44),
                  ("Cici",29,12,17,12),("Brody",28,7,21,21),("Esmeralda",27,10,17,51),
                  ("Kalea",26,10,16,18),("Suyou",26,14,12,5),("Mathilda",25,12,13,37),
                  ("Alice",25,10,15,24),("Freya",24,18,6,148),("Kimmy",24,12,12,16),
                  ("Melissa",23,10,13,52),("Gloo",22,13,9,36),("Novaria",21,10,11,11),
                  ("Miya",21,8,13,8),("Moskov",20,7,13,10),("Lylia",19,8,11,33),
                  ("Fanny",15,7,8,96),("Chou",15,6,9,9),("Harley",13,4,9,17),("Masha",12,8,4,69),
                  ("Ruby",12,7,5,11),("Vexana",12,7,5,4),("Lukas",11,5,6,10),("Badang",10,3,7,12),
                  ("Angela",10,4,6,10),("Phoveus",10,3,7,3),("Bruno",10,3,7,2),
                  ("Pharsa",10,8,2,2),("Yve",9,6,3,4),("Yi Sun-Shin",9,3,6,3),("Zetian",9,4,5,3),
                  ("Cecilion",8,1,7,5),("Harith",7,4,3,4),("Sora",7,3,4,4),("Kaja",6,4,2,11),
                  ("Dyrroth",6,3,3,8),("Karrie",6,3,3,0),("Hanabi",4,3,1,8),("Hilda",4,3,1,5),
                  ("Arlott",4,2,2,4),("Hayabusa",4,1,3,2),("Beatrix",4,3,1,2),("Khufra",4,3,1,1),
                  ("Aurora",3,2,1,3),("Estes",3,3,0,2),("Khaleed",3,1,2,1),("Lapu-lapu",3,2,1,0),
                  ("Yu Zhong",3,2,1,0),("Luo Yi",3,1,2,0),("Saber",2,1,1,3),("Hanzo",1,0,1,1),
                  ("Fredrinn",1,0,1,1),("Lolita",1,0,1,0),("Kagura",1,0,1,0),("Leomord",1,0,1,0),
                  ("Lunox",1,1,0,0),("Thamuz",1,0,1,0),("Granger",1,0,1,0),("Guinevere",1,0,1,0),
                  ("Ling",1,0,1,0),("Baxia",1,0,1,0),("Edith",1,1,0,0),("Xavier",1,0,1,0)])

# ---- MPL Indonesia S18 - 174 games -----------------------------------------
ID18 = dict(id="id", name="MPL Indonesia S18", short="ID", region="Indonesia",
            games=174, note="Current MPL ID season, and the deepest hero pool of the three.",
            rows=[("Paquito",87,39,48,58),("Hirara",84,45,39,80),("Belerick",68,34,34,20),
                  ("Claude",60,31,29,10),("Nolan",54,32,22,46),("Aulus",51,29,22,19),
                  ("Uranus",49,23,26,53),("Eudora",49,27,22,30),("Selena",46,19,27,48),
                  ("Zhuxin",46,23,23,43),("Atlas",43,24,19,120),("Obsidia",43,27,16,28),
                  ("Minotaur",43,18,25,28),("Freya",42,22,20,129),("Valentina",42,15,27,24),
                  ("Cici",40,21,19,17),("Carmilla",39,22,17,64),("Barats",39,18,21,43),
                  ("Rafaela",37,20,17,44),("Gloo",37,21,16,41),("Alice",35,19,16,19),
                  ("Melissa",34,18,16,53),("Kimmy",33,18,15,11),("Moskov",32,17,15,14),
                  ("Esmeralda",30,13,17,55),("Marcel",29,19,10,84),("Brody",28,8,20,13),
                  ("Lylia",27,13,14,27),("Miya",27,17,10,18),("Gatotkaca",27,16,11,11),
                  ("Mathilda",22,11,11,51),("Fanny",21,11,10,105),("Novaria",20,10,10,38),
                  ("Hylos",20,9,11,3),("Lukas",19,11,8,28),("Zetian",19,14,5,14),
                  ("Harley",18,6,12,12),("Badang",17,9,8,7),("Sora",17,7,10,7),("Alpha",16,9,7,5),
                  ("Phoveus",15,8,7,19),("Cecilion",15,10,5,7),("Suyou",15,5,10,1),
                  ("Yi Sun-shin",14,5,9,11),("Ruby",14,7,7,8),("Chou",14,4,10,7),
                  ("Masha",13,4,9,61),("Kalea",13,7,6,7),("Arlott",11,5,6,25),("Dyrroth",9,5,4,3),
                  ("Chip",7,1,6,22),("Clint",7,3,4,0),("Saber",6,4,2,4),("Hayabusa",6,2,4,3),
                  ("Yve",6,4,2,0),("Terizla",6,3,3,0),("Pharsa",6,2,4,0),("Lunox",5,1,4,2),
                  ("Hanabi",4,2,2,3),("Hanzo",4,2,2,3),("Leomord",4,2,2,1),("Kaja",3,1,2,10),
                  ("Guinevere",3,2,1,6),("Angela",3,0,3,3),("Fredrinn",3,1,2,2),("Bruno",3,2,1,1),
                  ("Hilda",3,3,0,0),("Valir",3,2,1,0),("Vexana",2,1,1,5),("Estes",2,1,1,1),
                  ("Wanwan",2,1,1,1),("Faramis",2,1,1,0),("Khaleed",2,1,1,0),("Argus",2,0,2,0),
                  ("Harith",2,0,2,0),("Joy",2,0,2,0),("Kadita",2,0,2,0),("Karrie",2,0,2,0),
                  ("Khufra",2,0,2,0),("Odette",2,0,2,0),("Ling",1,0,1,1),("Ixia",1,1,0,0),
                  ("Kagura",1,1,0,0),("Lapu-Lapu",1,1,0,0),("Edith",1,0,1,0),("Granger",1,0,1,0),
                  ("Lesley",1,0,1,0),("Luo Yi",1,0,1,0),("Minsitthar",1,0,1,0),
                  ("Tigreal",1,0,1,0),("Yu Zhong",1,0,1,0)])

# ---- MSL Myanmar S4 - 124 games --------------------------------------------
MM4 = dict(id="mm", name="MSL Myanmar S4", short="MM", region="Myanmar",
            games=124, note="Myanmar won Asian Games gold off the back of this league.",
            rows=[("Hirara",86,42,44,35),("Paquito",66,36,30,22),("Eudora",65,37,28,18),
                  ("Belerick",62,32,30,40),("Uranus",48,24,24,59),("Zhuxin",39,18,21,38),
                  ("Gloo",39,23,16,32),("Nolan",38,22,16,13),("Obsidia",33,14,19,18),
                  ("Minotaur",32,19,13,22),("Barats",31,12,19,27),("Carmilla",30,12,18,39),
                  ("Esmeralda",29,12,17,29),("Freya",27,17,10,96),("Brody",27,19,8,33),
                  ("Rafaela",27,13,14,24),("Miya",25,13,12,7),("Gatotkaca",24,12,12,9),
                  ("Selena",22,11,11,36),("Melissa",21,13,8,44),("Dyrroth",20,12,8,12),
                  ("Moskov",18,5,13,18),("Alice",18,9,9,16),("Zetian",18,8,10,2),
                  ("Aulus",17,7,10,23),("Yi Sun-shin",17,8,9,14),("Novaria",17,8,9,7),
                  ("Kimmy",16,8,8,6),("Atlas",15,6,9,98),("Marcel",15,7,8,93),("Chou",15,4,11,5),
                  ("Clint",15,8,7,3),("Masha",14,9,5,26),("Sora",14,7,7,7),("Claude",14,7,7,5),
                  ("Ruby",13,5,8,8),("Granger",13,7,6,3),("Fanny",12,7,5,41),("Cici",12,4,8,11),
                  ("Kalea",11,6,5,12),("Suyou",11,3,8,8),("Bruno",11,6,5,6),("Hylos",11,4,7,3),
                  ("Valentina",10,6,4,34),("Lylia",10,6,4,14),("Mathilda",9,5,4,13),
                  ("Phoveus",9,4,5,12),("Lukas",9,5,4,3),("Kaja",7,3,4,11),("Vexana",7,1,6,2),
                  ("Arlott",6,5,1,4),("Cecilion",6,2,4,3),("Leomord",6,2,4,3),("Harley",4,3,1,10),
                  ("Guinevere",4,3,1,4),("Angela",4,1,3,3),("Valir",4,4,0,2),("Aurora",4,2,2,0),
                  ("Khaleed",3,2,1,2),("Hanabi",3,0,3,2),("Harith",3,1,2,1),("Gord",3,2,1,0),
                  ("Tigreal",2,0,2,1),("Yu Zhong",2,1,1,0),("Beatrix",2,0,2,0),("Chip",1,1,0,12),
                  ("Badang",1,1,0,3),("Ixia",1,1,0,2),("Odette",1,0,1,2),("Kagura",1,0,1,1),
                  ("Lunox",1,0,1,1),("Faramis",1,1,0,0),("Jawhead",1,1,0,0),("Yve",1,1,0,0),
                  ("Argus",1,0,1,0),("Balmond",1,0,1,0),("Edith",1,0,1,0),("Karrie",1,0,1,0),
                  ("Pharsa",1,0,1,0),("Wanwan",1,0,1,0)])

LEAGUES = [AG2026, PH18, ID18, MM4]
