from flask import Flask, request, jsonify
import asyncio
from playwright.async_api import async_playwright

app = Flask(__name__)

async def get_bank_url(email_code):
    url = f"https://kiire.mpos.com/mailpos/#/{email_code}"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url, wait_until="load")
        await page.wait_for_timeout(3000)

        bank_url = await page.evaluate("""() => {
            const obj = window.localStorage.getItem("persist:payment");
            if (!obj) return null;
            const parsed = JSON.parse(obj);
            const payment = JSON.parse(parsed.payment);
            return payment?.bankUrl || null;
        }""")

        await browser.close()
        return bank_url

@app.route("/extract", methods=["GET"])
def extract():
    email_code = request.args.get("emailCode")
    if not email_code:
        return jsonify({"error": "emailCode requerido"}), 400

    bank_url = asyncio.run(get_bank_url(email_code))
    if not bank_url:
        return jsonify({"error": "bankUrl no encontrado"}), 404

    return jsonify({"bankUrl": bank_url})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
