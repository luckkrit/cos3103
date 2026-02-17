---
layout: section
transition: fade
---

# Application Demo

---

## Setup - .NET 10.0 SDK for Windows

<div class="w-fit mx-auto">

![2_68_app_sql_2026-02-18-02-13-49](/images/2_68_app_sql/2_68_app_sql_2026-02-18-02-13-49.png){.max-h-50vh}
</div>

---

## Setup - .NET 10.0 SDK for Windows (Cont.)

<div class="w-fit mx-auto">

![2_68_app_sql_2026-02-18-02-22-25](/images/2_68_app_sql/2_68_app_sql_2026-02-18-02-22-25.png){.max-h-50vh}
</div>

---

## Create Console Project

1. New Folder `mkdir pg-demo` and `cd pg-demo`

<div class="w-fit mx-auto">

![2_68_app_sql_2026-02-18-02-31-54](/images/2_68_app_sql/2_68_app_sql_2026-02-18-02-31-54.png){.max-h-40vh}
</div>

---

## Create Console Project

2. New Project `dotnet new pg-demo`

<div class="w-fit mx-auto">

![2_68_app_sql_2026-02-18-02-34-54](/images/2_68_app_sql/2_68_app_sql_2026-02-18-02-34-54.png){.max-h-45vh}
</div>

---

## Add Package Npgsql 

3. Add Package Npgsql `dotnet add package Npgsql`

<div class="w-fit mx-auto">

![2_68_app_sql_2026-02-18-02-37-13](/images/2_68_app_sql/2_68_app_sql_2026-02-18-02-37-13.png){.max-h-45vh}
</div>

---

## Edit Program.cs

```csharp
using Npgsql;
class Program
{
    static void Main()
    {
        string connString = "Host=localhost;Port=5432;Username=postgres;Password=password;Database=postgres";
        try{
            using var conn = new NpgsqlConnection(connString);
            conn.Open();
            string sql = "SELECT customernumber, customername FROM classicmodels.customers LIMIT 10";
            using var cmd = new NpgsqlCommand(sql, conn);
            using var reader = cmd.ExecuteReader();
            Console.WriteLine("\nCustomer List:");
            Console.WriteLine("ID\tName");
            Console.WriteLine(new string('-', 60));
            while (reader.Read())
            {
                Console.WriteLine($"{reader.GetInt32(0)}\t{reader.GetString(1)}");
            }
        }
        catch (Exception ex){
            Console.WriteLine($"✗ Connection failed: {ex.Message}");
        }
    }
}
```

---

## Run

4. Run app `dotnet run`

<div class="w-fit mx-auto">

![2_68_app_sql_2026-02-18-02-51-22](/images/2_68_app_sql/2_68_app_sql_2026-02-18-02-51-22.png){.max-h-45vh}
</div>

---

## Setup - Java & Maven

1. Install Java - https://www.oracle.com/asean/java/technologies/downloads/#java21
2. Install Maven - https://maven.apache.org/download.cgi
3. Download Maven for Windows - https://dlcdn.apache.org/maven/maven-3/3.9.12/binaries/apache-maven-3.9.12-bin.zip 
4. Extract Zip

---

## Setup - Java for Windows

5. Create `JAVA_HOME` to `C:\Program Files\Java\jdk-21\bin`
6. Add `C:\Program Files\Java\jdk-21\bin` to `PATH` 

<div class="w-fit mx-auto">

![2_68_app_sql_2026-02-18-03-53-15](/images/2_68_app_sql/2_68_app_sql_2026-02-18-03-53-15.png){.max-h-40vh}
</div>

---

## Setup - Maven for Windows

7. Create `MAVEN_HOME` to `C:\Users\luckk\Downloads\Compressed\apache-maven-3.9.12-bin\`
8. Add `C:\Users\luckk\Downloads\Compressed\apache-maven-3.9.12-bin\bin` to `PATH`  

<div class="w-fit mx-auto">

![2_68_app_sql_2026-02-18-03-44-14](/images/2_68_app_sql/2_68_app_sql_2026-02-18-03-44-14.png){.max-h-40vh}
</div>


---

## Setup - Maven for Windows (Cont.)

9. Test Maven


<div class="w-fit mx-auto">

![2_68_app_sql_2026-02-18-03-52-35](/images/2_68_app_sql/2_68_app_sql_2026-02-18-03-52-35.png){.max-h-45vh}
</div>

---

## Create Java App

`mvn archetype:generate`

<div class="w-fit mx-auto">

![keyviz_SPCo67jcKc](/images/2_68_app_sql/keyviz_SPCo67jcKc.gif){.max-h-50vh}

</div>

---

## Edit pom.xml

1. Add Postgres dependency

```xml

<dependencies>
    <!-- Previous Dependencies -->
    <!-- Postgresql -->
    <dependency>
      <groupId>org.postgresql</groupId>
      <artifactId>postgresql</artifactId>
      <version>42.7.1</version>
    </dependency>
</dependencies>
```

<div class="w-fit mx-auto">

![2_68_app_sql_2026-02-18-04-13-26](/images/2_68_app_sql/2_68_app_sql_2026-02-18-04-13-26.png){.max-h-25vh}
</div>

---

## Edit pom.xml (Cont.)

2. Add plugin

```xml
<plugins>
    <!-- Previous Plugins -->
    <!-- Execute App -->
    <plugin>
        <groupId>org.codehaus.mojo</groupId>
        <artifactId>exec-maven-plugin</artifactId>
        <version>3.1.0</version>
        <configuration>
            <mainClass>pgdemo.App</mainClass>
        </configuration>
    </plugin>
</plugins>
```

<div class="w-fit mx-auto">

![2_68_app_sql_2026-02-18-04-17-37](/images/2_68_app_sql/2_68_app_sql_2026-02-18-04-17-37.png){.max-h-25vh}
</div>

---
layout: two-cols-title
---

::title::
[Edit App.java]{class="text-2xl"}

::left::

```java

package pgdemo;
import java.sql.*;
public class App {
    public static void main(String[] args) {
        // PostgreSQL connection parameters
        String url = "jdbc:postgresql://localhost:5432/postgres";
        String username = "postgres";
        String password = "password";
        try (Connection conn = DriverManager.getConnection(url, username, password)) {
            System.out.println("Connected to PostgreSQL database!");
            // Create statement
            Statement stmt = conn.createStatement();
            // Execute query
            String sql = "SELECT * FROM classicmodels.customers LIMIT 5";
            ResultSet rs = stmt.executeQuery(sql);

```

::right::

```java

            // Get metadata
            ResultSetMetaData metadata = rs.getMetaData();
            int columnCount = metadata.getColumnCount();
            // Print column names
            for (int i = 1; i <= columnCount; i++) {
                System.out.print(metadata.getColumnName(i) + "\t");
            }
            System.out.println("\n" + "-".repeat(50));
            // Process results
            while (rs.next()) {
                for (int i = 1; i <= columnCount; i++) {
                    System.out.print(rs.getString(i) + "\t");
                }
                System.out.println();
            }
            rs.close();
            stmt.close();
            
        } catch (SQLException e) {
            System.err.println("Database error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

::default::

---

[Compile & Run]{class="text-2xl"}

- Compile `mvn compile`
- Run `mvn exec:java`

<div class="w-fit mx-auto">

![2_68_app_sql_2026-02-18-04-35-51](/images/2_68_app_sql/2_68_app_sql_2026-02-18-04-35-51.png){.max-h-40vh}
</div>