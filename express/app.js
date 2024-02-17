const express = require("express");
const multer = require("multer");
const { spawn } = require("child_process");

const port = 3501;
const app = express();
app.use(express.static(__dirname + "/public"));

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "./uploads");
  },
  filename: function (req, file, cb) {
    cb(null, "image.png");
  },
});

const upload = multer({ storage });

const runscript = (callback) => {
  console.log("running scripts");
  const python = spawn("python", ["../ocr.py"]);

  let data1 = "";

  python.stdout.on("data", function (data) {
    console.log("Received data from Python script:", data.toString());
    // Assuming you want to store data received from the script
    data1 += data.toString();
  });

  python.on("close", function (code) {
    console.log("Python script closed with code", code);
    // Assuming you want to return data to the route handler after the script finishes
    callback(data1);
  });

  python.on("error", function (err) {
    console.error("Error executing Python script:", err);
    // Assuming you want to handle errors in some way
    callback(null, err);
  });
};

app.post(
  "/profile-upload-single",
  upload.single("profile-file"),
  function (req, res, next) {
    console.log(JSON.stringify(req.file));
    var response = '<a href="/">Home</a><br>';
    response += "Files uploaded successfully.<br>";
    response += `<img src="${req.file.path}" /><br>`;

    // Run the Python script
    runscript((data, err) => {
      if (err) {
        console.error("Error running script:", err);
        return res.status(500).json({ error: "Error running script" });
      }
      const responseData = data.replace(/\r?\n|\r/g, "");
      // Send response with data received from the script
      return res.json({ data: responseData });
    });
  }
);

app.post(
  "/profile-upload-multiple",
  upload.array("profile-files", 12),
  function (req, res, next) {
    var response = '<a href="/">Home</a><br>';
    response += "Files uploaded successfully.<br>";
    for (var i = 0; i < req.files.length; i++) {
      response += `<img src="${req.files[i].path}" /><br>`;
    }

    return res.send(response);
  }
);

app.listen(port, () => console.log(`Server running on port ${port}!`));
