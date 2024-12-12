import tkinter as tk
from tkinter import ttk 
from PIL import Image, ImageTk
from tkinter import messagebox, StringVar, Tk, Label 
import mysql.connector  # Import mysql.connector for MySQL database connection
import bcrypt 

import tkinter as tk
from tkinter import messagebox
 # For Treeview and Scrollbar
import mysql.connector


class HousingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Serchie: Housing Finder")
        self.root.geometry("1200x800")
        self.root.iconbitmap('logo.ico')
        self.role_var = tk.StringVar()

        # Establish the database connection to MySQL
        self.conn = mysql.connector.connect(
            host='localhost',         
            user='root',               
            password='',       
            database='housing_db'      
        )
        self.cursor = self.conn.cursor()  # Create a cursor to execute SQL queries

        # Create table if it doesn't exist
        self.create_table()

        # UI Components (Role Selection)
        self.role_var = StringVar(value="tenant")  # Default to tenant
        self.current_role = None

        # Show the role selection screen
        self.show_role_selection()

    def create_table(self):
        """Create tables if they don't exist."""
        self.cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS landlords (
            LandlordID INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
        ''')
        self.cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS listings (
            listingID INT AUTO_INCREMENT PRIMARY KEY,
            address VARCHAR(255),
            price DECIMAL(10, 2),
            housing_type VARCHAR(50),
            contact_info VARCHAR(255),
            LandlordID INT,
            FOREIGN KEY (LandlordID) REFERENCES landlords(LandlordID)
        )
        ''')
        self.conn.commit()
            
    def clear_window(self):
        """Clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_role_selection(self):
        """Display the role selection screen with a unique background for Home Menu."""
        # Clear existing widgets
        self.clear_window()

        # Create a frame for the left side with role selection and login
        left_frame = tk.Frame(self.root, bg="#1ABC9C", width=700, height=800)
        left_frame.pack(side="left", fill="both", expand=True)

        # Add a title to the left frame
        tk.Label(
            left_frame, 
            text="Select Your Role:", 
            font=("Verdana", 18, "bold"), 
            bg="#1ABC9C", 
            fg="black",
            pady=100
        ).pack()

        # Add buttons for role selection
        tenant_button = tk.Button(
            left_frame, 
            text="Tenant", 
            font=("Arial", 30, "bold"), 
            width=10, 
            command=self.open_tenant_interface, 
            bg="#F39C12", 
            fg="black", 
            relief="flat"
        )
        tenant_button.pack(pady=5)

        landlord_button = tk.Button(
            left_frame, 
            text="Landlord", 
            font=("Arial", 30, "bold"), 
            width=10, 
            command=self.open_landlord_interface, 
            bg="#F39C12",
            fg="black",
            relief="flat"
        )
        landlord_button.pack(pady=5)

        # Add hover effects
        tenant_button.bind("<Enter>", self.on_enter)
        tenant_button.bind("<Leave>", self.on_leave)
        landlord_button.bind("<Enter>", self.on_enter)
        landlord_button.bind("<Leave>", self.on_leave)

        # Create a frame for the right side with the description of the platform
        right_frame = tk.Frame(self.root, bg="#34495E", width=600, height=800)
        right_frame.pack(side="right", fill="both", expand=True)

        # Title in the right frame
        tk.Label(
            right_frame, 
            text="Serchie: Housing Finder", 
            font=("Montserrat", 28, "bold"), 
            fg="white", 
            bg="#34495E"
        ).pack(pady=100)

        # Description text in the right frame
        description = """
            A platform that helps people to look and promotes their houses. 
            For users who want to find a house, they will select the tenant 
            interface to search for their preferred choices. 
            Meanwhile, the landlord can input the necessary details for their houses, 
            so tenants can be informed about house choices they will have.
            """
    
        tk.Label(
            right_frame, 
            text=description, 
            font=("Arial", 18), 
            fg="#219ebc", 
            bg="#34495E", 
            justify="left", 
            padx=20, 
            pady=5
        ).pack()


    def on_enter(self, event):
        """Change button color on hover."""
        event.widget.config(bg="#F1C40F")

    def on_leave(self, event):
        """Reset button color after hover."""
        event.widget.config(bg="#F39C12")

    def login(self):
        """Handle login process."""
        print("Login clicked")


    def clear_window(self):
        """Clear the current UI components from the main window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        """Handles login and navigates based on role selection."""
        role = self.role_var.get()

        if role != self.current_role:
            self.current_role = role
            if role == "tenant":
                self.open_tenant_interface()
            elif role == "landlord":
                self.open_landlord_interface()

    def open_tenant_interface(self):
        """Opens the tenant interface to search for properties."""
        self.clear_window()
        self.root.config(bg="lightblue")  # Light blue background for Tenant Interface

        housing_type_var = StringVar(value="Apartment")
        price_var = StringVar(value="Select Price Range")

        # Tenant Interface UI
        tk.Label(self.root, text="Welcome to the Tenant Interface!", font=("Arial", 22), bg="lightblue").grid(row=0, columnspan=2, pady=20)

        # Housing Type Selection
        self.housing_type_var = StringVar(value='Apartment')
        tk.Label(self.root, text="Housing Type:", font=("Arial", 20), bg="lightblue").grid(row=1, column=0, padx=18, pady=15, sticky="e")
        housing_options = ['Apartment', 'Bedspace', 'House']
        housing_type_menu = tk.OptionMenu(self.root, self.housing_type_var, *housing_options)
        housing_type_menu.config(font=("Arial", 18),bg="#f5f5f1", width=18)  
        housing_type_menu.grid(row=1, column=1, padx=18, pady=18)

        # Location entry
        tk.Label(self.root, text="Location:", font=("Arial", 20), bg="lightblue").grid(row=2, column=0, padx=15, pady=10, sticky="e")
        self.location_entry = tk.Entry(self.root,bg="#f5f5f1", font=("Arial", 18))
        self.location_entry.grid(row=2, column=1, padx=15, pady=10)

        # Preferred Budget entry
        self.price_var = StringVar(value='Preferred Price Range')
        tk.Label(self.root, text="Price:", font=("Arial", 20), bg="lightblue").grid(row=3, column=0, padx=15, pady=10, sticky="e")
        budget_options = ["1500-2500", "2500-4000", "4000-8000", "8000+"]
        budget_entry = tk.OptionMenu(self.root, self.price_var, *budget_options)
        budget_entry.config(bg="#f5f5f1" ,font=("Arial", 18), width=18)  
        budget_entry.grid(row=3, column=1, padx=15, pady=10)

        # Button to search for housing
        tk.Button(self.root, text="Find Housing", command=self.find_housing, font=("Arial", 20), bg ="#2196F3", width=15).grid(row=4, columnspan=2, pady=15)

        # Results display area
        self.result_text = tk.Text(self.root, height=10, width=100, bg="#8ecae6", font=("Arial", 16))
        self.result_text.grid(row=5, columnspan=2, padx=15, pady=15)

        # Return button
        tk.Button(self.root, text="Return", command=self.show_role_selection, font=("Arial", 20), bg ="#ff4d4d",  width=15).grid(row=6, columnspan=2, pady=15)

    def find_housing(self):
        """Search for housing based on criteria entered by the tenant."""
        housing_type = self.housing_type_var.get()
        location = self.location_entry.get().strip()
        price_range = self.price_var.get().strip()  

        # Validate the budget input
        price_mapping = {
            "1500-2500": (1500, 2500),
            "2500-4000": (2500, 4000),
            "4000-8000": (4000, 8000),
            "8000+": (8000, 999999999)
        }
        if price_range not in price_mapping:
            messagebox.showwarning("Invalid Input", "Please select a valid price range.")
            return
        min_price, max_price = price_mapping[price_range]

        # Default values for housing type and location
        housing_type = "%" if housing_type == "Select Housing Type" else housing_type
        location = "%" if not location else f"%{location}%"

        # Fetch properties that match the criteria
        try:
            self.cursor.execute(
                '''
                SELECT listingID, address, price, housing_type, contact_info, LandlordID 
                FROM listings 
                WHERE housing_type LIKE %s AND address LIKE %s AND price BETWEEN %s AND %s
                ''',
                (housing_type, location, min_price, max_price)
            )
            properties = self.cursor.fetchall()

            # Update Treeview with results
            self.result_text.delete(1.0, tk.END)
            if properties:
                for prop in properties:
                    self.result_text.insert(tk.END, f"ID: {prop[0]} | {prop[1]} - ₱{prop[2]} - {prop[3]} | Contact: {prop[4]} | LandlordID: {prop[5]}\n")
            else:
                self.result_text.insert(tk.END, "No properties found matching your criteria.")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error fetching properties: {e}")


    def open_landlord_interface(self):
        """Opens the landlord interface to manage properties."""
        self.clear_window()
        self.root.config(bg="#669999")

        tk.Label(self.root, text="Landlord Login", font=("Arial", 32), bg="#669999").pack(pady=70)

        # Username input
        tk.Label(self.root, text="Username:", font=("Arial", 18), bg="#669999").pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=("Arial", 18), width=25)
        self.username_entry.pack(pady=5)

        # Password input
        tk.Label(self.root, text="Password:", font=("Arial", 18), bg="#669999").pack(pady=5)
        self.password_entry = tk.Entry(self.root, font=("Arial", 18), show="*", width=25)
        self.password_entry.pack(pady=5)

        # Buttons for Login and Sign-up
        tk.Button(self.root, text="Login", command=self.landlord_login, font=("Arial", 18), bg = "#4CAF50",  width=15).pack(pady=10)
        tk.Button(self.root, text="Sign Up", command=self.landlord_signup, font=("Arial", 18),bg ="#2196F3", width=15).pack(pady=10)
        
        # Return to Role Selection
        tk.Button(self.root, text="Return", command=self.show_role_selection, font=("Arial", 18),bg ="#ff4d4d", width=15).pack(pady=20)

    def landlord_signup(self):
        """Sign-up functionality for landlords."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
            return

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            self.cursor.execute("INSERT INTO landlords (username, password) VALUES (%s, %s)", (username, hashed_password))
            self.conn.commit()
            messagebox.showinfo("Sign Up Successful", "Account created successfully! Please log in.")
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Username already exists. Please choose a different one.")

    def landlord_login(self):
        """Login functionality for landlords."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
            return

        # Check the database for the username
        self.cursor.execute("SELECT LandlordID, password FROM landlords WHERE username = %s", (username,))
        result = self.cursor.fetchone()

        if result:
            landlord_id, stored_password = result
            # Verify the password
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                self.current_landlord_id = landlord_id  # Store the landlord ID
                messagebox.showinfo("Login Successful", "Welcome, Landlord!")
                self.open_landlord_dashboard()
            else:
                messagebox.showerror("Error", "Invalid password. Please try again.")
        else:
            messagebox.showerror("Error", "Username not found.")


    def edit_property(self):
        """Edit selected property details."""
        selected_item = self.properties_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a property to edit.")
            return

        # Get the values of the selected item
        item_values = self.properties_tree.item(selected_item)['values']
        
        # Create edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Property")
        edit_window.geometry("500x600")
        edit_window.configure(bg="lightgreen")
        
        # Property Type Selection
        tk.Label(edit_window, text="Housing Type:", font=("Arial", 16), bg="lightgreen").pack(pady=10)
        housing_type_var = StringVar(value=item_values[2])
        housing_type_menu = tk.OptionMenu(edit_window, housing_type_var, 'Apartment', 'Bedspace', 'House')
        housing_type_menu.config(font=("Arial", 14), width=15)
        housing_type_menu.pack(pady=5)

        # Price entry
        tk.Label(edit_window, text="Price:", font=("Arial", 16), bg="lightgreen").pack(pady=10)
        price_entry = tk.Entry(edit_window, font=("Arial", 14))
        price_entry.insert(0, item_values[1].replace('₱', ''))
        price_entry.pack(pady=5)

        # Location entry
        tk.Label(edit_window, text="Location:", font=("Arial", 16), bg="lightgreen").pack(pady=10)
        location_entry = tk.Entry(edit_window, font=("Arial", 14))
        location_entry.insert(0, item_values[0])
        location_entry.pack(pady=5)

        # Contact Info entry
        tk.Label(edit_window, text="Contact Info:", font=("Arial", 16), bg="lightgreen").pack(pady=10)
        contact_entry = tk.Entry(edit_window, font=("Arial", 14))
        contact_entry.insert(0, item_values[3])
        contact_entry.pack(pady=5)

        def save_changes():
            try:
                # Update database
                self.cursor.execute('''
                    UPDATE listings 
                    SET address = %s, price = %s, housing_type = %s, contact_info = %s
                    WHERE address = %s AND price = %s AND housing_type = %s AND contact_info = %s
                ''', (
                    location_entry.get(),
                    float(price_entry.get()),
                    housing_type_var.get(),
                    contact_entry.get(),
                    item_values[0],
                    float(item_values[1].replace('₱', '')),
                    item_values[2],
                    item_values[3]
                ))
                self.conn.commit()
                
                # Update treeview
                self.properties_tree.item(selected_item, values=(
                    location_entry.get(),
                    f"₱{price_entry.get()}",
                    housing_type_var.get(),
                    contact_entry.get()
                ))
                
                messagebox.showinfo("Success", "Property updated successfully!")
                edit_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid price.")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error updating property: {e}")

        # Save button
        tk.Button(
            edit_window,
            text="Save Changes",
            command=save_changes,
            font=("Arial", 16),
            bg="#4CAF50",
            fg="white",
            width=15
        ).pack(pady=20)

    def open_landlord_dashboard(self):
        """Landlord dashboard for managing properties."""
        self.clear_window()
        self.root.config(bg="#67de65")
        
        main_label = tk.Label(self.root, text="Welcome to the Landlord Dashboard!", font=("Arial", 22), bg="#67de65")
        main_label.pack(pady=20)

        # Create container frame for better organization
        container = tk.Frame(self.root, bg="#67de65")
        container.pack(fill="both", expand=True, padx=20)

        # Left side for input fields
        left_frame = tk.Frame(container, bg="#67de65")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Right side for displaying available properties
        right_frame = tk.Frame(container, bg="#67de65")
        right_frame.pack(side="right", fill="both", expand=True)

        # Landlord Interface UI
        tk.Label(left_frame, text="Landlord Interface", font=("Arial", 22), bg="#67de65").grid(row=0, columnspan=2, pady=10)

        # Property Type Selection
        self.housing_type_var = StringVar(value='Apartment')
        tk.Label(left_frame, text="Housing Type:", font=("Arial", 18), bg="#67de65").grid(row=1, column=0, padx=18, pady=18, sticky="e")
        housing_type_menu = tk.OptionMenu(left_frame, self.housing_type_var,'Apartment', 'Bedspace', 'House')
        housing_type_menu.grid(row=1, column=1, padx=18, pady=18)  
        housing_type_menu.config(font=("Arial", 18), width=18)

        # Price entry
        tk.Label(left_frame, text="Price:", font=("Arial", 20), bg="#67de65").grid(row=2, column=0, padx=15, pady=10, sticky="e")
        self.price_entry = tk.Entry(left_frame, font=("Arial", 18))
        self.price_entry.grid(row=2, column=1, padx=15, pady=10)

        # Location entry
        tk.Label(left_frame, text="Location:", font=("Arial", 20), bg="#67de65").grid(row=3, column=0, padx=15, pady=10, sticky="e")
        self.location_entry = tk.Entry(left_frame, font=("Arial", 18))
        self.location_entry.grid(row=3, column=1, padx=15, pady=10)

        # Contact Name entry
        tk.Label(left_frame, text="Your Name:", font=("Arial", 20), bg="#67de65").grid(row=4, column=0, padx=15, pady=10, sticky="e")
        self.contact_name_entry = tk.Entry(left_frame, font=("Arial", 18))
        self.contact_name_entry.grid(row=4, column=1, padx=15, pady=10)

        # Contact Number entry
        tk.Label(left_frame, text="Contact Number:", font=("Arial", 20), bg="#67de65").grid(row=5, column=0, padx=15, pady=10, sticky="e")
        self.contact_number_entry = tk.Entry(left_frame, font=("Arial", 18))
        self.contact_number_entry.grid(row=5, column=1, padx=15, pady=10)

        # Button Frame for better organization
        button_frame = tk.Frame(left_frame, bg="#67de65")
        button_frame.grid(row=6, columnspan=2, pady=20)

        # Add property button
        tk.Button(
            button_frame,
            text="Add Property",
            command=self.add_property,
            font=("Arial", 18),
            width=22,
            bg="#36ff00",
            fg="black"
        ).pack(pady=5)

        # Show properties button
        tk.Button(
            button_frame,
            text="Show Available Properties",
            command=self.show_properties,
            font=("Arial", 18),
            width=22
        ).pack(pady=10)

        # Edit property button
        tk.Button(
            button_frame,
            text="Edit Selected Property",
            command=self.edit_property,
            font=("Arial", 18),
            width=22,
            bg="#2196F3",
            fg="white"
        ).pack(pady=10)

        # Delete property button
        tk.Button(
            button_frame,
            text="Delete Selected Property",
            command=self.delete_property,
            font=("Arial", 18),
            width=22,
            bg="#ff4d4d",
            fg="white"
        ).pack(pady=10)

        # Return button
        tk.Button(
            button_frame,
            text="Return",
            command=self.show_role_selection,
            font=("Arial", 18),
            width=22
        ).pack(pady=10)

        # Create Treeview with scrollbar
        self.properties_tree = ttk.Treeview(right_frame, columns=('ID', 'Location', 'Price', 'Type', 'Contact'), show='headings')
        self.properties_tree.heading('ID', text='ID')
        self.properties_tree.heading('Location', text='Location')
        self.properties_tree.heading('Price', text='Price')
        self.properties_tree.heading('Type', text='Housing Type')
        self.properties_tree.heading('Contact', text='Contact Info')

        # Set column widths
        self.properties_tree.column('ID', width=50)
        self.properties_tree.column('Location', width=150)
        self.properties_tree.column('Price', width=100)
        self.properties_tree.column('Type', width=50)
        self.properties_tree.column('Contact', width=200)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.properties_tree.yview)
        self.properties_tree.configure(yscroll=scrollbar.set)
        
        # Pack Treeview and Scrollbar
        self.properties_tree.pack(padx=20, pady=20, expand=True, fill='both')

    def delete_property(self):
        """Delete selected property from the database."""
        selected_item = self.properties_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a property to delete.")
            return

        # Get the values of the selected item
        item_values = self.properties_tree.item(selected_item)['values']
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the property at {item_values[0]}?"):
            try:
                # Delete from database
                self.cursor.execute('''
                    DELETE FROM listings 
                    WHERE address = %s AND price = %s AND housing_type = %s AND contact_info = %s
                ''', (item_values[0], float(item_values[1].replace('₱', '')), item_values[2], item_values[3]))
                self.conn.commit()
                
                # Remove from treeview
                self.properties_tree.delete(selected_item)
                messagebox.showinfo("Success", "Property deleted successfully!")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error deleting property: {e}")

            
    def add_property(self):
        """Add property to the database."""
        property_type = self.housing_type_var.get()
        price = self.price_entry.get()
        location = self.location_entry.get()
        contact_name = self.contact_name_entry.get()
        contact_number = self.contact_number_entry.get()

        # Validate input
        if not all([price, location, contact_name, contact_number]):
            messagebox.showwarning("Input Error", "Please fill in all fields!")
            return

        try:
            price = float(price)
        except ValueError:
            messagebox.showwarning("Price Error", "Please enter a valid price.")
            return

        # Insert the property into the database
        self.cursor.execute(''' 
            INSERT INTO listings (address, price, housing_type, contact_info, LandlordID)
            VALUES (%s, %s, %s, %s, %s)
        ''', (location, price, property_type, f"{contact_name} | {contact_number}", self.current_landlord_id))
        self.conn.commit()

        messagebox.showinfo("Property Added", "Your property has been added successfully!")


    def show_properties(self):
        """Show properties added by the landlord."""
        for item in self.properties_tree.get_children():
            self.properties_tree.delete(item)

        # Fetch properties from the database
        self.cursor.execute("SELECT listingID, address, price, housing_type, contact_info FROM listings")
        properties = self.cursor.fetchall()

        # Insert properties into the Treeview
        if properties:
            for prop in properties:
                self.properties_tree.insert('', 'end', values=(prop[0], prop[1], f"₱{prop[2]}", prop[3], prop[4]))
        else:
            messagebox.showinfo("Properties", "No properties added yet.")


    def close(self):
        """Close the database connection before exiting the program."""
        try:
            if self.conn:
                self.conn.close()  # Close the MySQL connection
                print("Database connection closed.")
        except Exception as e:
            print(f"Error closing database connection: {e}")
        finally:
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = HousingApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)  # Ensure connection is closed when the window is closed
    root.mainloop()
