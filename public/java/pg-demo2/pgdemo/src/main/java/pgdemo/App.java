package pgdemo;
import java.sql.*;

public class App {
    public static void main(String[] args) {
        // PostgreSQL connection parameters
        String url = "jdbc:postgresql://localhost:5432/postgres";
        String username = "postgres";
        String password = "password";

        String sql = "SELECT * FROM classicmodels.customers LIMIT 5";

        try (Connection conn = DriverManager.getConnection(url, username, password);
             Statement stmt = conn.createStatement(); // In try(....) when error occurred, it will close automatically
             ResultSet rs = stmt.executeQuery(sql)) {

            System.out.println("Connected to PostgreSQL database!");

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

        } catch (SQLException e) {
            System.err.println("Database error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}