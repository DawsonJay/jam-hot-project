--
-- PostgreSQL database dump
--

\restrict 0enk4cudxblkpR3Y5bLSb7b5J0hOvC3LtYuqydCchpcc8Bs7lcxHJcduJX7bGGB

-- Dumped from database version 15.14 (Debian 15.14-1.pgdg13+1)
-- Dumped by pg_dump version 16.10 (Ubuntu 16.10-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: fruits; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fruits (
    id integer NOT NULL,
    fruit_name character varying(100) NOT NULL,
    ai_identifier character varying(100) NOT NULL,
    created_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.fruits OWNER TO postgres;

--
-- Name: profiles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.profiles (
    fruit_id integer NOT NULL,
    scientific_name character varying(100),
    description text,
    flavor_profile jsonb,
    jam_uses jsonb,
    season character varying(50),
    storage_tips text,
    nutrition jsonb,
    created_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.profiles OWNER TO postgres;

--
-- Name: fruit_coverage; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.fruit_coverage AS
 SELECT f.id,
    f.fruit_name,
    f.ai_identifier,
        CASE
            WHEN (p.fruit_id IS NOT NULL) THEN 'covered'::text
            ELSE 'not_covered'::text
        END AS coverage_status,
    p.description,
    p.flavor_profile
   FROM (public.fruits f
     LEFT JOIN public.profiles p ON ((f.id = p.fruit_id)));


ALTER VIEW public.fruit_coverage OWNER TO postgres;

--
-- Name: fruits_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fruits_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.fruits_id_seq OWNER TO postgres;

--
-- Name: fruits_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.fruits_id_seq OWNED BY public.fruits.id;


--
-- Name: recipe_fruits; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.recipe_fruits (
    recipe_id integer NOT NULL,
    fruit_id integer NOT NULL,
    is_primary boolean DEFAULT false
);


ALTER TABLE public.recipe_fruits OWNER TO postgres;

--
-- Name: recipes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.recipes (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    ingredients jsonb NOT NULL,
    instructions jsonb NOT NULL,
    rating numeric(3,2) NOT NULL,
    review_count integer NOT NULL,
    source character varying(100) NOT NULL,
    source_url text NOT NULL,
    image_url text NOT NULL,
    servings character varying(50),
    prep_time character varying(50),
    cook_time character varying(50),
    total_time character varying(50),
    created_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    scraped_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.recipes OWNER TO postgres;

--
-- Name: recipe_summary; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.recipe_summary AS
 SELECT r.id,
    r.title,
    r.rating,
    r.review_count,
    r.source,
    r.image_url,
    string_agg((f.fruit_name)::text, ', '::text ORDER BY rf.is_primary DESC) AS fruits,
    count(rf.fruit_id) AS fruit_count
   FROM ((public.recipes r
     JOIN public.recipe_fruits rf ON ((r.id = rf.recipe_id)))
     JOIN public.fruits f ON ((rf.fruit_id = f.id)))
  GROUP BY r.id, r.title, r.rating, r.review_count, r.source, r.image_url;


ALTER VIEW public.recipe_summary OWNER TO postgres;

--
-- Name: recipes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.recipes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.recipes_id_seq OWNER TO postgres;

--
-- Name: recipes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.recipes_id_seq OWNED BY public.recipes.id;


--
-- Name: fruits id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fruits ALTER COLUMN id SET DEFAULT nextval('public.fruits_id_seq'::regclass);


--
-- Name: recipes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recipes ALTER COLUMN id SET DEFAULT nextval('public.recipes_id_seq'::regclass);


--
-- Data for Name: fruits; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fruits (id, fruit_name, ai_identifier, created_date) FROM stdin;
1	strawberry	strawberry	2025-09-21 22:17:57.541301
2	blueberry	blueberry	2025-09-21 22:17:57.541301
3	apple	apple	2025-09-21 22:17:57.541301
4	lemon	lemon	2025-09-21 22:17:57.541301
5	orange	orange	2025-09-21 22:17:57.541301
6	peach	peach	2025-09-21 22:17:57.541301
7	blackberry	blackberry	2025-09-21 22:17:57.541301
8	raspberry	raspberry	2025-09-21 22:17:57.541301
9	cherry	cherry	2025-09-21 22:17:57.541301
10	grape	grape	2025-09-21 22:17:57.541301
\.


--
-- Data for Name: profiles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.profiles (fruit_id, scientific_name, description, flavor_profile, jam_uses, season, storage_tips, nutrition, created_date) FROM stdin;
1	Fragaria × ananassa	Sweet, juicy berries perfect for jams and preserves	{"tart": 6, "sweet": 8, "acidic": 4, "floral": 3}	["jam", "preserves", "compote", "syrup"]	Summer	Store in refrigerator for up to 5 days. Freeze for longer storage.	{"fiber": "2g", "sugar": "4.9g", "calories": 32, "vitamin_c": "58mg"}	2025-09-21 22:17:57.542551
\.


--
-- Data for Name: recipe_fruits; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.recipe_fruits (recipe_id, fruit_id, is_primary) FROM stdin;
1	1	t
1	4	f
\.


--
-- Data for Name: recipes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.recipes (id, title, ingredients, instructions, rating, review_count, source, source_url, image_url, servings, prep_time, cook_time, total_time, created_date, scraped_date) FROM stdin;
1	Classic Strawberry Jam	[{"unit": "cups", "quantity": "4", "ingredient": "strawberries"}, {"unit": "cups", "quantity": "3", "ingredient": "sugar"}, {"unit": "tbsp", "quantity": "1", "ingredient": "lemon juice"}]	["Wash and hull strawberries", "Combine strawberries and sugar in large pot", "Bring to boil, add lemon juice", "Cook until thickened", "Ladle into sterilized jars"]	4.50	127	Allrecipes	https://www.allrecipes.com/recipe/classic-strawberry-jam	https://images.media-allrecipes.com/images/classic-strawberry-jam.jpg	Makes 4 half-pint jars	20 minutes	15 minutes	\N	2025-09-21 22:17:57.543587	2025-09-21 22:17:57.543587
\.


--
-- Name: fruits_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fruits_id_seq', 10, true);


--
-- Name: recipes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.recipes_id_seq', 1, true);


--
-- Name: fruits fruits_ai_identifier_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fruits
    ADD CONSTRAINT fruits_ai_identifier_key UNIQUE (ai_identifier);


--
-- Name: fruits fruits_fruit_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fruits
    ADD CONSTRAINT fruits_fruit_name_key UNIQUE (fruit_name);


--
-- Name: fruits fruits_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fruits
    ADD CONSTRAINT fruits_pkey PRIMARY KEY (id);


--
-- Name: profiles profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profiles
    ADD CONSTRAINT profiles_pkey PRIMARY KEY (fruit_id);


--
-- Name: recipe_fruits recipe_fruits_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recipe_fruits
    ADD CONSTRAINT recipe_fruits_pkey PRIMARY KEY (recipe_id, fruit_id);


--
-- Name: recipes recipes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recipes
    ADD CONSTRAINT recipes_pkey PRIMARY KEY (id);


--
-- Name: idx_fruits_ai_identifier; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fruits_ai_identifier ON public.fruits USING btree (ai_identifier);


--
-- Name: idx_fruits_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fruits_name ON public.fruits USING btree (fruit_name);


--
-- Name: idx_recipe_fruits_fruit_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_recipe_fruits_fruit_id ON public.recipe_fruits USING btree (fruit_id);


--
-- Name: idx_recipe_fruits_fruit_primary; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_recipe_fruits_fruit_primary ON public.recipe_fruits USING btree (fruit_id, is_primary);


--
-- Name: idx_recipe_fruits_primary; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_recipe_fruits_primary ON public.recipe_fruits USING btree (is_primary) WHERE (is_primary = true);


--
-- Name: idx_recipe_fruits_recipe_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_recipe_fruits_recipe_id ON public.recipe_fruits USING btree (recipe_id);


--
-- Name: idx_recipes_rating; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_recipes_rating ON public.recipes USING btree (rating DESC);


--
-- Name: idx_recipes_rating_reviews; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_recipes_rating_reviews ON public.recipes USING btree (rating DESC, review_count DESC);


--
-- Name: idx_recipes_review_count; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_recipes_review_count ON public.recipes USING btree (review_count DESC);


--
-- Name: idx_recipes_source; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_recipes_source ON public.recipes USING btree (source);


--
-- Name: profiles profiles_fruit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profiles
    ADD CONSTRAINT profiles_fruit_id_fkey FOREIGN KEY (fruit_id) REFERENCES public.fruits(id);


--
-- Name: recipe_fruits recipe_fruits_fruit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recipe_fruits
    ADD CONSTRAINT recipe_fruits_fruit_id_fkey FOREIGN KEY (fruit_id) REFERENCES public.fruits(id);


--
-- Name: recipe_fruits recipe_fruits_recipe_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recipe_fruits
    ADD CONSTRAINT recipe_fruits_recipe_id_fkey FOREIGN KEY (recipe_id) REFERENCES public.recipes(id);


--
-- PostgreSQL database dump complete
--

\unrestrict 0enk4cudxblkpR3Y5bLSb7b5J0hOvC3LtYuqydCchpcc8Bs7lcxHJcduJX7bGGB

