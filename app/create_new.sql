create table sports_facility (
    id integer not null,
    facility_name VARCHAR(200) not null,
    capacity integer not null,
    start_time VARCHAR(5) not null,
    end_time VARCHAR(5) not null,
    is_classes integer not null default 0,
    PRIMARY KEY (id)
);

INSERT INTO sports_facility (facility_name, capacity, start_time, end_time)
VALUES ('Swimming pool', 30, '08:00', '20:00');

INSERT INTO sports_facility (facility_name, capacity, start_time, end_time)
VALUES ('Fitness Room', 35, '08:00', '22:00');

INSERT INTO sports_facility (facility_name, capacity, start_time, end_time)
VALUES ('Squash court', 4, '08:00', '22:00');

INSERT INTO sports_facility (facility_name, capacity, start_time, end_time)
VALUES ('Sports hall', 45, '08:00', '22:00');

INSERT INTO sports_facility (facility_name, capacity, start_time, end_time)
VALUES ('Climbing Wall', 22, '10:00', '20:00');

INSERT INTO sports_facility (facility_name, capacity, start_time, end_time, is_classes)
VALUES ('Studio', 25, '08:00', '22:00', 1);

create table sports_activity (
    id integer not null,
    facility_id integer,
    activity_name VARCHAR(200) not null,
    is_team integer not null default 0,
    duration integer not null,
    unit integer not null,
    price NUMERIC(10,2) not null,
    PRIMARY KEY (id), 
    FOREIGN KEY(facility_id) REFERENCES sports_facility (id)
);

INSERT INTO sports_activity (facility_id, activity_name, is_team, duration, unit, price)
VALUES (1, 'General use', 0, 1, 1, 7);

INSERT INTO sports_activity (facility_id, activity_name, is_team, duration, unit, price)
VALUES (1, 'Lane Swimming', 0, 1, 1, 7);

INSERT INTO sports_activity (facility_id, activity_name, is_team, duration, unit, price)
VALUES (1, 'Lessons', 0, 1, 1, 7);

INSERT INTO sports_activity (facility_id, activity_name, is_team, duration, unit, price)
VALUES (1, 'Team events', 1, 2, 30, 7);

INSERT INTO sports_activity (facility_id, activity_name, is_team, duration, unit, price)
VALUES (2, 'General use', 0, 1, 1, 7);

INSERT INTO sports_activity (facility_id, activity_name, is_team, duration, unit, price)
VALUES (3, '1-hour sessions', 0, 1, 2, 7);

INSERT INTO sports_activity (facility_id, activity_name, is_team, duration, unit, price)
VALUES (4, '1-hour sessions', 0, 1, 1, 7);

INSERT INTO sports_activity (facility_id, activity_name, is_team, duration, unit, price)
VALUES (4, 'Team events', 1, 2, 45, 7);

INSERT INTO sports_activity (facility_id, activity_name, is_team, duration, unit, price)
VALUES (5, 'General use', 0, 1, 1, 7);

INSERT INTO sports_activity (facility_id, activity_name, is_team, duration, unit, price)
VALUES (6, 'Exercise classes', 0, 1, 1, 7);

create table sports_activity_class (
    id integer NOT NULL,
    sports_activity_id integer,
    class_name VARCHAR(100) NOT NULL,
    day_of_week integer not null,
    start_time VARCHAR(5) NOT NULL,
    end_time VHARCHAR(5) NOT NULL,
    PRIMARY KEY (id),
    foreign key (sports_activity_id) references sports_activity(id)
);

INSERT INTO sports_activity_class (sports_activity_id, class_name, day_of_week, start_time, end_time)
VALUES (4, 'Swimming', 5, '08:00', '10:00');

INSERT INTO sports_activity_class (sports_activity_id, class_name, day_of_week, start_time, end_time)
VALUES (4, 'Swimming', 0, '08:00', '10:00');

INSERT INTO sports_activity_class (sports_activity_id, class_name, day_of_week, start_time, end_time)
VALUES (8, 'Sports hall', 4, '07:00', '09:00');

INSERT INTO sports_activity_class (sports_activity_id, class_name, day_of_week, start_time, end_time)
VALUES (8, 'Sports hall', 6, '09:00', '11:00');

INSERT INTO sports_activity_class (sports_activity_id, class_name, day_of_week, start_time, end_time)
VALUES (10, 'Pilates', 1, '18:00', '19:00');

INSERT INTO sports_activity_class (sports_activity_id, class_name, day_of_week, start_time, end_time)
VALUES (10, 'Aerobics', 2, '18:00', '11:00');

INSERT INTO sports_activity_class (sports_activity_id, class_name, day_of_week, start_time, end_time)
VALUES (10, 'Aerobics', 4, '07:00', '08:00');

INSERT INTO sports_activity_class (sports_activity_id, class_name, day_of_week, start_time, end_time)
VALUES (10, 'Aerobics', 6, '10:00', '11:00');

INSERT INTO sports_activity_class (sports_activity_id, class_name, day_of_week, start_time, end_time)
VALUES (10, 'Yoga', 5, '07:00', '08:00');

INSERT INTO sports_activity_class (sports_activity_id, class_name, day_of_week, start_time, end_time)
VALUES (10, 'Yoga', 0, '09:00', '10:00');

CREATE TABLE sports_booking (
    id integer not null,
    user_id integer not null,
    facility_id integer not null,
    activity_id integer not null,
    class_id integer null,
    payment_id integer not null,
    start_time DATETIME not null,
    end_time DATETIME not null,
    price NUMERIC(10,2) not null,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (facility_id) REFERENCES sports_facility(id),
    FOREIGN KEY (activity_id) REFERENCES sports_activity(id),
    FOREIGN KEY (payment_id) REFERENCES payment(payment_id),
    FOREIGN KEY (class_id) REFERENCES sports_activity_class(id)
);
