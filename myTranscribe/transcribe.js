import cors from "cors";
import express from "express";
import multer from "multer";
import fetch from "node-fetch";
import fs from "fs";
import dotenv from "dotenv";

dotenv.config();
const app = express();
app.use(cors({ origin: "https://66nihaal44.github.io" }));
const upload = multer({ dest: "uploads/" });
app.post("/transcribe", upload.single("file"), async (req, res) => {
  try{
    const fileStream = fs.createReadStream(req.file.path);
    const response = await fetch("http//localhost:5001", {
      method: "POST",
      body: (() => {
        const form = new FormData();
        form.append("file", fileStream, req.file.originalname);
        return form;
      })()
    });
    const data = await response.json();
    res.json({ text: data.text });
    fs.unlinkSync(req.file.path);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Transcription failed." });
  }
});
app.listen(3000, () => console.log("Server running on http://localhost:3000"));
app.use(express.static("public"));
