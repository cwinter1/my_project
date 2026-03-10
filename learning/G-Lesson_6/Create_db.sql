USE master
IF NOT EXISTS (
   SELECT name
   FROM sys.databases
   WHERE name = N'TutorialDB'
)
CREATE DATABASE [TutorialDB]
GO
USE TutorialDB;
SELECT DB_NAME() AS [Current Database]; 

/***********************************************************
-- Create a new table called 'TableName' in schema 'SchemaName'
-- Drop the table if it already exists

IF OBJECT_ID('SchemaName.TableName', 'U') IS NOT NULL
DROP TABLE SchemaName.TableName
GO

***********************************************************/

-- Create the table in the specified schema
IF OBJECT_ID('dbo.Employees', 'U') IS NOT NULL
drop table Employees
CREATE TABLE dbo.Employees
(
    EmployeeId INT NOT NULL PRIMARY KEY,
    Name [NVARCHAR](50)  NOT NULL,
    Location [NVARCHAR](50)  NOT NULL
    -- specify more columns here
);
GO
drop table Study
CREATE TABLE dbo.Study
(
    EmployeeId INT NOT NULL PRIMARY KEY,
    Name [VARCHAR](8000)  NOT NULL,
    Location [NVARCHAR](50)  NOT NULL
    -- specify more columns here
);

INSERT INTO Employees
   ([EmployeeId],[Name],[Location])
VALUES
   ( 1, N'Jared', N'Australia'),
   ( 2, N'Nikita', N'India'),
   ( 3, N'Tom', N'Germany'),
   ( 4, N'Jake', N'United States')
GO

-- Select statements
SELECT * 
FROM Study

SELECT * 
FROM Employees