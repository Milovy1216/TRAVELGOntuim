CREATE TABLE IF NOT EXISTS USER (
    user_id VARCHAR(10) PRIMARY KEY NOT NULL,
    user_name TEXT NOT NULL,
    email TEXT,
    profile_pic BLOB,
    sign_up_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS TRIP (
    trip_id VARCHAR(10) PRIMARY KEY NOT NULL,
    trip_name TEXT NOT NULL,
    is_public BOOLEAN NOT NULL,
    description TEXT,
    create_date DATE NOT NULL,
    create_by VARCHAR(10) NOT NULL,
    collect_date DATE DEFAULT CURRENT_TIMESTAMP,
    host VARCHAR(10) NOT NULL,
    FOREIGN KEY (create_by) REFERENCES USER(user_id),
    FOREIGN KEY (host) REFERENCES USER(user_id)
);

CREATE TABLE IF NOT EXISTS SPOT (
    spot_id VARCHAR(10) PRIMARY KEY NOT NULL,
    spot_name TEXT NOT NULL,
    ave_rate DOUBLE CHECK (rating >= 1 AND rating <= 5),
    address TEXT NOT NULL,
    category TEXT NOT NULL,
    estimate_cost INTEGER NOT NULL,
    is_public BOOLEAN NOT NULL,
    estimate_stay_time INTEGER,
    create_by VARCHAR(10) NOT NULL,
    create_time DATE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (create_by) REFERENCES USER(user_id)
);

CREATE TABLE IF NOT EXISTS FRIENDSHIP (
    user_id1 VARCHAR(10) NOT NULL,
    user_id2 VARCHAR(10) NOT NULL,
    friend_begin_date DATE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id1, user_id2),
    FOREIGN KEY (user_id1) REFERENCES USER(user_id),
    FOREIGN KEY (user_id2) REFERENCES USER(user_id)
);

CREATE TABLE IF NOT EXISTS PARTICIPATEIN (
    trip_id VARCHAR(10) NOT NULL,
    participant_id VARCHAR(10) NOT NULL,
    PRIMARY KEY (trip_id, participant_id),
    FOREIGN KEY (trip_id) REFERENCES TRIP(trip_id),
    FOREIGN KEY (participant_id) REFERENCES USER(user_id)
);

CREATE TABLE IF NOT EXISTS SPOTINTRIP (
    trip_id VARCHAR(10) NOT NULL,
    spot_id VARCHAR(10) NOT NULL,
    sequence_number INTEGER NOT NULL,
    PRIMARY KEY (trip_id, sequence_number),
    FOREIGN KEY (trip_id) REFERENCES TRIP(trip_id),
    FOREIGN KEY (spot_id) REFERENCES SPOT(spot_id)
);

CREATE TABLE IF NOT EXISTS COMMENT (
    user_id VARCHAR(10) NOT NULL,
    spot_id VARCHAR(10) NOT NULL,
    rate INTEGER CHECK (rate >= 1 AND rate <= 5),
    comment_date DATE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, spot_id),
    FOREIGN KEY (user_id) REFERENCES USER(user_id),
    FOREIGN KEY (spot_id) REFERENCES SPOT(spot_id)
);

CREATE TABLE IF NOT EXISTS SPOTCOLLECT (
    user_id VARCHAR(10) NOT NULL,
    spot_id VARCHAR(10) NOT NULL,
    collect_date DATE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, spot_id),
    FOREIGN KEY (user_id) REFERENCES USER(user_id),
    FOREIGN KEY (spot_id) REFERENCES SPOT(spot_id)
);

CREATE TABLE IF NOT EXISTS TRIPCOLLECT (
    user_id VARCHAR(10) NOT NULL,
    trip_id VARCHAR(10) NOT NULL,
    collect_date DATE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, trip_id),
    FOREIGN KEY (user_id) REFERENCES USER(user_id),
    FOREIGN KEY (trip_id) REFERENCES TRIP(trip_id)
);