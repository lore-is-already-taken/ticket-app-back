CREATE TABLE IF NOT EXISTS User (
    userID SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Rol (
    rolID SERIAL PRIMARY KEY,
    userID INT REFERENCES User(userID),
    rol VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Ticket (
    ticketID SERIAL PRIMARY KEY,
    autor INT REFERENCES User(userID) NOT NULL,
    responsable INT REFERENCES User(userID),
    contenido VARCHAR(255) NOT NULL,
    categoria VARCHAR(255) NOT NULL,
    review INT,
    prioridad INT NOT NULL,
    textoReview VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Evento (
    eventoID SERIAL PRIMARY KEY,
    ticketID INT REFERENCES Ticket(ticketID) NOT NULL,
    contenido VARCHAR(255) NOT NULL,
);
