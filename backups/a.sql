toc.dat                                                                                             0000600 0004000 0002000 00000002711 14157600051 0014437 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        PGDMP           1    	            y            dbsup    14.1 (Debian 14.1-1.pgdg110+1)    14.1 (Debian 14.1-1.pgdg110+1)     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false         �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false         �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false         �           1262    16384    dbsup    DATABASE     Y   CREATE DATABASE dbsup WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.utf8';
    DROP DATABASE dbsup;
                pgsup    false         �          0    16385    alembic_version 
   TABLE DATA           6   COPY public.alembic_version (version_num) FROM stdin;
    public          pgsup    false    209       3314.dat �          0    16391    user 
   TABLE DATA           �   COPY public."user" (id, username, password, first_name, last_name, middle_name, innerphone, phone, email, superuser) FROM stdin;
    public          pgsup    false    211       3316.dat �           0    0    user_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.user_id_seq', 1, false);
          public          pgsup    false    210                                                               3314.dat                                                                                            0000600 0004000 0002000 00000000022 14157600051 0014235 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        79d01da172b2
\.


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              3316.dat                                                                                            0000600 0004000 0002000 00000000005 14157600051 0014240 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        \.


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           restore.sql                                                                                         0000600 0004000 0002000 00000003667 14157600051 0015377 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        --
-- NOTE:
--
-- File paths need to be edited. Search for $$PATH$$ and
-- replace it with the path to the directory containing
-- the extracted data files.
--
--
-- PostgreSQL database dump
--

-- Dumped from database version 14.1 (Debian 14.1-1.pgdg110+1)
-- Dumped by pg_dump version 14.1 (Debian 14.1-1.pgdg110+1)

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

DROP DATABASE dbsup;
--
-- Name: dbsup; Type: DATABASE; Schema: -; Owner: pgsup
--

CREATE DATABASE dbsup WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.utf8';


ALTER DATABASE dbsup OWNER TO pgsup;

\connect dbsup

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
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: pgsup
--

COPY public.alembic_version (version_num) FROM stdin;
\.
COPY public.alembic_version (version_num) FROM '$$PATH$$/3314.dat';

--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: pgsup
--

COPY public."user" (id, username, password, first_name, last_name, middle_name, innerphone, phone, email, superuser) FROM stdin;
\.
COPY public."user" (id, username, password, first_name, last_name, middle_name, innerphone, phone, email, superuser) FROM '$$PATH$$/3316.dat';

--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgsup
--

SELECT pg_catalog.setval('public.user_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         