create Table Employee(
    id serial primary key,
    name varchar(50),
    email varchar(50),
    salary numeric(10,2),
    gender varchar default 'male',
    age int,
    created_at timestamp default current_timestamp
);


insert into employee (name,email,salary,gender,age) values ('hamza','hamza@gmail.com',35000,'male',25);

INSERT INTO employee (name, email, salary, gender, age)
VALUES
('alex', 'alex@gmail.com', 30000, 'male', 22),
('john', 'john@gmail.com', 55000, 'male', 28),
('sarah', 'sarah@gmail.com', 60000, 'female', 29),
('david', 'david@gmail.com', 40000, 'male', 26),
('priya', 'priya@gmail.com', 48000, 'female', 24),
('rohan', 'rohan@gmail.com', 70000, 'male', 32),
('emma', 'emma@gmail.com', 52000, 'female', 27),
('mike', 'mike@gmail.com', 38000, 'male', 23);

-- 23 age , 45 salary

SELECT gender, COUNT(*)
FROM Employee
GROUP BY gender;

select avg(salary) from employee group by gender;


create table asset(asset_name varchar(50),asset_type varchar(50),asset_cost int,is_service Boolean,is_assigned Boolean, employeeid int references employee(id));

INSERT INTO asset (asset_name, asset_type, asset_cost, is_service, is_assigned, employeeid)
VALUES
('safaa', 'safaa@gmail.com', 45000, 'female', 31),
('MacBook Pro', 'Laptop', 120000, TRUE, TRUE, 1),
('Dell Monitor', 'Monitor', 18000, FALSE, TRUE, 2),
('Office Chair', 'Furniture', 8000, FALSE, TRUE, 3),
('AWS Hosting', 'Cloud Service', 15000, TRUE, FALSE, 4),
('Keyboard', 'Accessory', 2500, FALSE, TRUE, 5),
('Microsoft 365', 'Software', 6000, TRUE, FALSE, 6),
('HP Printer', 'Printer', 22000, FALSE, TRUE, 7),
('Internet Connection', 'Network Service', 3000, TRUE, FALSE, 8),
('iPhone 16', 'Mobile', 85000, FALSE, TRUE, 9);


select asset_name from asset where is_service = FALSE and asset_name like 'Dell%';

name, email, salary, asset 

SELECT e.name, e.email, e.salary, a.asset_name
FROM employee e
INNER JOIN asset a
ON e.id = a.employeeid;

