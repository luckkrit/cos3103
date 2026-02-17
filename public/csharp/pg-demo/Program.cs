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
