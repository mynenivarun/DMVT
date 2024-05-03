# DMVT
Data Migration &amp; Validation Tool


The DMVT is a tool designed to assist users in migrating data from one cloud provider to
another. As users often switch between cloud providers due to factors such as pricing, availability
zones, and reliability, this tool provides a secure and efficient way to migrate data between
different cloud provider databases. The DMVT aims to ensure no data loss occurs during the
migration process and to save time through the use of a single Python script.

The script follows these steps:
1. Establishes a connection with the source and destination cloud provider databases.
2. Migrates data from the old cloud provider database to the new cloud provider database.
3. Validates the migrated data to ensure all data has been transferred correctly.
4. Generates a report detailing the migration process, including the amount of data migrated
and the validation results.

The migration process involves establishing a secure, encrypted connection between the source
and destination databases, reading data from the source database, and inserting it into the
destination database. If the migration is successful, the script proceeds to the validation stage.

During validation, the script checks the connection status and re-establishes the connection if
necessary. Then reads data from both the source and destination databases, comparing them from
start to finish. If the comparison fails, the script prompts the user to delete all data in the
destination database and initiates a re-migration. If the validation is successful, the script
generates a report on the migration and validation process.
