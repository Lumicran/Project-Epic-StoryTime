--
-- PostgreSQL database dump
--

-- Dumped from database version 10.5 (Ubuntu 10.5-0ubuntu0.18.04)
-- Dumped by pg_dump version 10.5 (Ubuntu 10.5-0ubuntu0.18.04)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public.players DROP CONSTRAINT players_user_id_fkey;
ALTER TABLE ONLY public.players DROP CONSTRAINT players_games_played_fkey;
ALTER TABLE ONLY public.players DROP CONSTRAINT players_games_not_played_fkey;
ALTER TABLE ONLY public.game_masters DROP CONSTRAINT game_masters_user_id_fkey;
ALTER TABLE ONLY public.game_masters DROP CONSTRAINT game_masters_created_games_fkey;
ALTER TABLE ONLY public.game_information DROP CONSTRAINT game_information_game_id_fkey;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
ALTER TABLE ONLY public.players DROP CONSTRAINT players_pkey;
ALTER TABLE ONLY public.games DROP CONSTRAINT games_pkey;
ALTER TABLE ONLY public.game_masters DROP CONSTRAINT game_masters_pkey;
ALTER TABLE ONLY public.game_information DROP CONSTRAINT game_information_pkey;
ALTER TABLE public.users ALTER COLUMN user_id DROP DEFAULT;
ALTER TABLE public.players ALTER COLUMN player_id DROP DEFAULT;
ALTER TABLE public.games ALTER COLUMN game_id DROP DEFAULT;
ALTER TABLE public.game_masters ALTER COLUMN gm_id DROP DEFAULT;
ALTER TABLE public.game_information ALTER COLUMN game_info_id DROP DEFAULT;
DROP SEQUENCE public.users_user_id_seq;
DROP TABLE public.users;
DROP SEQUENCE public.players_player_id_seq;
DROP TABLE public.players;
DROP SEQUENCE public.games_game_id_seq;
DROP TABLE public.games;
DROP SEQUENCE public.game_masters_gm_id_seq;
DROP TABLE public.game_masters;
DROP SEQUENCE public.game_information_game_info_id_seq;
DROP TABLE public.game_information;
DROP EXTENSION plpgsql;
DROP SCHEMA public;
--
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA public;


--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: game_information; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.game_information (
    game_info_id integer NOT NULL,
    game_id integer NOT NULL,
    event_order integer NOT NULL,
    latitude numeric NOT NULL,
    longitude numeric NOT NULL,
    location_hint text,
    story_text text NOT NULL,
    puzzle text NOT NULL,
    puzzle_key text NOT NULL,
    puzzle_hint text,
    weather_condition character varying(64)
);


--
-- Name: game_information_game_info_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.game_information_game_info_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: game_information_game_info_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.game_information_game_info_id_seq OWNED BY public.game_information.game_info_id;


--
-- Name: game_masters; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.game_masters (
    gm_id integer NOT NULL,
    user_id integer,
    created_games integer
);


--
-- Name: game_masters_gm_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.game_masters_gm_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: game_masters_gm_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.game_masters_gm_id_seq OWNED BY public.game_masters.gm_id;


--
-- Name: games; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.games (
    game_id integer NOT NULL,
    game_name character varying(64) NOT NULL,
    game_description text
);


--
-- Name: games_game_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.games_game_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: games_game_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.games_game_id_seq OWNED BY public.games.game_id;


--
-- Name: players; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.players (
    player_id integer NOT NULL,
    user_id integer,
    games_played integer,
    games_not_played integer
);


--
-- Name: players_player_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.players_player_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: players_player_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.players_player_id_seq OWNED BY public.players.player_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    fname character varying(64),
    lname character varying(64),
    username character varying(64) NOT NULL,
    email character varying(64) NOT NULL,
    password character varying(64) NOT NULL,
    security_question character varying(64) NOT NULL,
    security_answer character varying(64) NOT NULL
);


--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: game_information game_info_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.game_information ALTER COLUMN game_info_id SET DEFAULT nextval('public.game_information_game_info_id_seq'::regclass);


--
-- Name: game_masters gm_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.game_masters ALTER COLUMN gm_id SET DEFAULT nextval('public.game_masters_gm_id_seq'::regclass);


--
-- Name: games game_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.games ALTER COLUMN game_id SET DEFAULT nextval('public.games_game_id_seq'::regclass);


--
-- Name: players player_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.players ALTER COLUMN player_id SET DEFAULT nextval('public.players_player_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: game_information; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.game_information (game_info_id, game_id, event_order, latitude, longitude, location_hint, story_text, puzzle, puzzle_key, puzzle_hint, weather_condition) FROM stdin;
1	1	1	1	1	Show up at the fountain at Santana Row.	Your partner walks ahead, holding the leash of your pet cat. The main plaza opens up, and you see a large fountain, ringed with shrubbery. The bushes start to rustle...	Do cats have thumbs?	No	Can a cat open a door?	light_rain
2	1	2	1	2	Walk past the fountain at Santana Row.	Cats jump out of the bushes with their thumbless paws, their tails standing up rod-straight. Several leave the pack and run to form a ring around you and your honey. The scruffiest cat steps forward and...	What is the legal max amount of cats you can own in SJ?	4	Less than 5.	None
3	2	1	5	5	Walk to the beach end in Santa Cruz.	You and your partner reach the edge of Dogs Beach, rumored to have a roaming pack of viscious dogs. As you look out into the sunset, you hear barking from a distance. You realize that you've both lingered too long, and start jogging back up the length of the coast. As you break out into a sprint, you see...	Do dogs have thumbs?	No	Can a dog open a door?	light_rain
4	1	3	500	600	Walk past the corridor, into the main street.	He starts speaking, in a voice contrary to his appearance. Silvery smooth, he berates you for only owning ONE cat when you are legally allowed to own up to FOUR! After his lecture, he begins to...	Does a cats' purr vibrate their body?	Yes	Sounds are vibrations in the air.	no_condition
5	2	2	950	-200	Walk back up the length of the beach.	Hundreds of dogs race out from the distance, their thumbless paws hitting the ground faster and faster. They corner the both of you, hemming you into the shoreline. As you tremble in fear...	How many breeds of dogs are there?	Many	A lot!	no_condition
6	3	1	37.3797849	-121.9431958	Walk outside of the South Bay Hackbright campus.	The sun sank in the west, setting a curtain of darkness as it left. You look out the window, and see shadows squiggling around the campus. A shudder ripples through you as you turn away abruptly from the window. You've spent the last couple hours banging out code for your project. Unfortunately, there is little to show. You sigh in defeat and pack up for the day, heading out while the rest of of your cohort members work diligently. As you walk through the hallway, you count the doors lining the hallway.	How many doors are there between Hackbright's room and the stairs?	7	More than 6, less than 8.	no_condition
7	3	2	37.379185	-121.940723	Walk towards the Indian restaurant.	...5...6...7 rooms are passed as you walk towards the exit. Taking a large leap, you hop down the stairs, two steps at a time. Curling around the banister, you push out the front doors and feel a wave of chilly air hit your entire body. The temperature was -oddly- a little too cold for an average California fall night. The wind picks up and a curling meow resounds as you stand still, shivering. A black cat slinks from a bush, eyeing you. Its left eye appears golden-green, while its right is a pale blue. It mournfully meows again and turns towards the Indian restaurant, one of the few dining options in the area. As it walks away, it beckons you to follow with its tail. On a whim, you decide to follow it...	What is the medical condition where an individual has differently colored eyes?	Heterochromia	Multi-color-noun suffix	no_condition
8	3	3	37.379863	-121.941118	Walk from the restaurant towards De La Cruz Blvd, where the lot entrance is.	The cat comes to a stop in front of the restaurant, turns to look at you balefully, and sprints off to the right. You look at the dark building in unease. At this time, it should've still been open, hosting large amounts of people. But today, not a single person could be seen in the near vicinity. The wind picks up, carrying along with it a rancid odor. You think to yourself that the restaurant shouldn't be tossing used its' garbage so carelessly. You hear shuffling sounds coming from Hackbright, and turn around to greet fellow classmates - only, it's not them. You feel sharp alarm as you see raggedly dressed men walking towards you. A hollow pit forms at the bottom of your stomach and grows as they get closer. You slowly turn to your left, towards the street, and walk at a reasonable pace towards the street...	What is the cross street in which the South Bay Hackbright Academy is located on?	De La Cruz Blvd	This street crosses W Trimble Road.	no_condition
9	3	4	37.379936	-121.940164	Cross the street over to where Cooks Collision is.	You reach De La Cruz Blvd, and look back carefully to see if the men are still there. You see them back in the distance. Relief washes over you as you notice several similarly dressed women join the group. They all look like they're still walking towards you, so you take a right at the street and continue until you're in sight of W Trimble Road. At the crosswalk, you push the walking button and wait patiently as the lights turn colors. Finally, the light changes and you're able to cross the street, over to Cooks Collision. Midway through the crosswalk, the same black cat peeks out from the shrubbery in front of the office, throwing another meow in your direction. You speed up to catch up to the cat...	How many cat breeds does the "Cat Fanciers Association's" directory list that have "black" as a color option?	19	More than a dozen, less than 2 dozen.	no_condition
\.


--
-- Data for Name: game_masters; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.game_masters (gm_id, user_id, created_games) FROM stdin;
1	1	1
2	1	2
\.


--
-- Data for Name: games; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.games (game_id, game_name, game_description) FROM stdin;
1	Cats Attack	Cats attack an unsuspecting couple.
2	Dogs Attack	Dogs attack a suspecting couple.
3	Hackbright Midnight Adventure	A supernatural event occurs at Hackbright Academy in the middle of project month.
\.


--
-- Data for Name: players; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.players (player_id, user_id, games_played, games_not_played) FROM stdin;
1	2	1	2
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (user_id, fname, lname, username, email, password, security_question, security_answer) FROM stdin;
1	Mac	Earl	fish	macearl@gmail.com	b474a99a2705e23cf905a484ec6d14ef58b56bbe62e9292783466ec363b5072d	When was the lst time you caught the flu?	2018
2	Cali	Co	cat	calico@gmail.com	77af778b51abd4a3c51c5ddd97204a9c3ae614ebccb75a606c3b6865aed6744e	What is your favorite pets' name?	cat
3	Gir	Affe	giraffe	giraffe@gmail.com	6bb7e067447139b18f6094d2d15bcc264affde89a8b9f5227fe5b38abd8b19d7	What is your favorite flower?	daisy
4	Kila	Minjaro	mountain	kilaminjaro@gmail.com	3b80d38f7686a8b5f8e61ad562ec069ac172732fb4dab946401f21a438669a4b	What is your favorite pets' name?	dog
5	Li	On	lion	lion@gmail.com	fc59487712bbe89b488847b77b5744fb6b815b8fc65ef2ab18149958edb61464	What is your favorite flower?	sunflower
\.


--
-- Name: game_information_game_info_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.game_information_game_info_id_seq', 10, true);


--
-- Name: game_masters_gm_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.game_masters_gm_id_seq', 3, true);


--
-- Name: games_game_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.games_game_id_seq', 4, true);


--
-- Name: players_player_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.players_player_id_seq', 1, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_user_id_seq', 6, true);


--
-- Name: game_information game_information_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.game_information
    ADD CONSTRAINT game_information_pkey PRIMARY KEY (game_info_id);


--
-- Name: game_masters game_masters_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.game_masters
    ADD CONSTRAINT game_masters_pkey PRIMARY KEY (gm_id);


--
-- Name: games games_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_pkey PRIMARY KEY (game_id);


--
-- Name: players players_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.players
    ADD CONSTRAINT players_pkey PRIMARY KEY (player_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: game_information game_information_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.game_information
    ADD CONSTRAINT game_information_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.games(game_id);


--
-- Name: game_masters game_masters_created_games_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.game_masters
    ADD CONSTRAINT game_masters_created_games_fkey FOREIGN KEY (created_games) REFERENCES public.games(game_id);


--
-- Name: game_masters game_masters_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.game_masters
    ADD CONSTRAINT game_masters_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: players players_games_not_played_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.players
    ADD CONSTRAINT players_games_not_played_fkey FOREIGN KEY (games_not_played) REFERENCES public.games(game_id);


--
-- Name: players players_games_played_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.players
    ADD CONSTRAINT players_games_played_fkey FOREIGN KEY (games_played) REFERENCES public.games(game_id);


--
-- Name: players players_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.players
    ADD CONSTRAINT players_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: -
--

GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

