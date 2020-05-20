drop table if exists Users;
drop table if exists User_Roles;
drop table if exists Roles;
drop table if exists Order_Item;
drop table if exists User_Orders;
drop table if exists CustomerEmail;
drop table if exists LogoImages;

CREATE TABLE Users(
        email           TEXT,
        password        TEXT,
        name            TEXT,
        PRIMARY KEY(email)
);

CREATE TABLE User_Roles(
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id         TEXT,
        role_id         INTEGER,
        FOREIGN KEY (user_id) REFERENCES Users (email)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        FOREIGN KEY (role_id) REFERENCES Roles (id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
);

CREATE TABLE Roles(
        id          TEXT,
        name        TEXT,
        PRIMARY KEY(id)
);

CREATE TABLE Order_Item(
        id               INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id         INTEGER,
        product_name        TEXT,
        product_size        TEXT,
        price               TEXT,
        quantity         INTEGER,
        product_img_src     TEXT,
        design              TEXT,
        FOREIGN KEY (order_id) REFERENCES User_Orders (id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
);

CREATE TABLE User_Orders(
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id        TEXT,
        paypal_order_id  TEXT,
        address        TEXT,
        FOREIGN KEY (user_id) REFERENCES Users (email)
                ON UPDATE CASCADE
                ON DELETE CASCADE
);

CREATE TABLE CustomerEmail(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email       TEXT
);

CREATE TABLE LogoImages(
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        file_path       TEXT
);

CREATE TABLE Discounts(
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT,
        amount      INTEGER,
        type        TEXT
);