create table CONTRAVENTIONS (
  id integer primary key,
  proprietaire varchar(100),
  categorie varchar(50),
  etablissement varchar(100),
  adresse text,
  ville varchar(500),
  description varchar(100),
  date_infraction text,
  date_jugement text,
  montant integer
);

create table users (
  id integer primary key,
  utilisateur varchar(25),
  email varchar(100),
  salt varchar(32),
  hash varchar(128),
  surveillerEtab varchar(500), 
  photo blob
);

create table sessions (
  id integer primary key,
  id_session varchar(32),
  utilisateur varchar(25)
);


