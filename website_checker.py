import tkinter as tk
from tkinter import messagebox
import whois
import validators
import requests

def check_website():
    url = entry_url.get()
    
    if not validators.url(url):
        messagebox.showerror("Invalid URL", "Please enter a valid URL.")
        return
    
    try:
        # WHOIS lookup
        domain_info = whois.whois(url)
        domain_age = (domain_info.expiration_date - domain_info.creation_date).days
        is_ssl = requests.get(url).url.startswith("https")
        
        # Display results
        result = f"""
        Domain: {domain_info.domain_name}
        Registrar: {domain_info.registrar}
        Creation Date: {domain_info.creation_date}
        Expiration Date: {domain_info.expiration_date}
        SSL Secured: {'Yes' if is_ssl else 'No'}
        Domain Age: {domain_age} days
        """
        messagebox.showinfo("Website Info", result)
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch website information: {e}")

# GUI Setup
root = tk.Tk()
root.title("Website Scam Checker")

tk.Label(root, text="Enter Website URL:").pack(pady=5)
entry_url = tk.Entry(root, width=50)
entry_url.pack(pady=5)

tk.Button(root, text="Check Website", command=check_website).pack(pady=20)

root.mainloop()


from flask import Flask, render_template, request
import whois
import validators

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def check_website():
    if request.method == 'POST':
        url = request.form['url']
        if validators.url(url):
            try:
                domain_info = whois.whois(url)
                return f"Domain Name: {domain_info.domain_name}<br>Registrar: {domain_info.registrar}"
            except Exception as e:
                return f"Error: {e}"
        return "Invalid URL"

    return '''
        <form method="post">
            Enter URL: <input type="text" name="url">
            <input type="submit">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
