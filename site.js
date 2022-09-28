// *setting up database for username,psw,profile img, ect... AND setting up login/register functions
console.log("hi, welcome to WEB-1. I see you're looking at the code. I wouldn't really trust it since it is my first website but you can get some inspiration from it.");
function getIdP(id, ih) {
    document.getElementById(id).innerHTML=ih
}
function getClassP(id,ih) {
    document.getElementsByClassName(id).innerHTML= ih
}

// const sqlite3 = require('sqlite3')
// let sql = 'INSERT INTO userData(Username, Password) VALUES(?,?,?,?,?)';
// let row3 = 'SELECT User-ID FROM userDATA'

// function userId() {
//   let userId = row3
//   userId++ 
//   return userId
// }

// !open database in memory
// let db = new sqlite3.Database('./User-DATA-DB.db', sqlite3.OPEN_READWRITE, (err) => {
//   if (err) {
//     console.error(err.message);
//   }
//   console.log('Connected to the database.');
// });

// if (document.URL.includes('register.html')){
  
//   //!Variables for INPUT
//   let Email = document.getElementById("Email-register").value || 'UNDEFINED';
//   let Name = document.getElementById("Name-register").value || 'UNDEFINED';
//   let UserName = document.getElementById("Username-register").value || 'UNDEFINED';
//   let Password = document.getElementById("Password-register").value || 'UNDEFINED';  
  
//   document.getElementsByName('btn-register-1').onclick = function () {
//     console.log('btn-register-1 Pressed');
//     sql = 'INSERT INTO userData(Username, Password, User-ID, Name, EMAIL) VALUES(?,?,?,?,?)';
  
//     db.run(
//     sql, 
//     [UserName, Password, userId, Name, Email], 
//     (err) => {
//     if (err) return console.error(err.message)
    
//     console.log('DATA ADDED')
//     }); 
//   };
// };



// sql = 'SELECT * FROM userData';

// db.all(sql, [], (err, rows)=>{
//   if (err) return console.error(err.message)

//   rows.forEach(row => {
//     console.log(row)
//   });
// })

// // !close the database connection
// db.close((err) => {
//   if (err) {
//     return console.error(err.message);
//   }
//   console.log('Close the database connection.');
// });

//* app code below, database code above

//! Page DATA

//* LOGIN AND REGISTER PAGES
// if (document.URL.includes("login.html")) {
//  let empty = true 
// }

//* OTHER PAGES

if (document.URL.includes("len.html")) {
    console.log("you are in the len page");

    function Hide(UNIT) {
        let un = 'undefined';
        if (UNIT === un ) {
            document.getElementsByClassName("ans-text").visibility = "hidden";
        } if (
            UNIT === 'm' || UNIT === 'M' ||
            UNIT === 'km' || UNIT === 'KM' ||
            UNIT === 'cm' || UNIT === 'CM' ||
            UNIT === 'yd' || UNIT === 'YD' ||
            UNIT === 'FT' || UNIT === 'ft' ||
            UNIT === "MI" || UNIT === "mi"
        ) {
            document.getElementById('BTN-1-LEN-IF').style.visibility = "hidden";
        };
    };
    let UNIT = document.getElementById('UNIT-LEN').value || 'undefined';
    Hide(UNIT);

    function Len() {
        let NUM = document.getElementById('NUM-LEN').value || 1;
        let UNIT = document.getElementById('UNIT-LEN').value || 'undefined';
        console.log("btn 'BTN-1-LEN' pressed.");
        console.log(NUM)
        console.log(UNIT)
        //* Meters
        if (UNIT === 'm' || UNIT === 'M') {
            getClassP("len-1-text",  "M to KM");
            getClassP("len-2-text", "M to CM");
            getClassP("len-3-text", "M to FT");
            getClassP("len-4-text", "M to YD");
            getClassP("len-5-text",  "M to MI");
            getClassP("len-6-text", "M to IN");

            getIdP("01-len") = (UNIT / 1000);
            getIdP("02-len") = (UNIT * 100);
            getIdP("03-len") = (UNIT * 3.28);
            getIdP("04-len") = (UNIT * 1.094);
            getIdP("05-len") = (UNIT / 1809);
            getIdP("06-len") = (UNIT * 39.37);

            getClassP('ans-text-NUM') = NUM;

            getIdP("len-1-formula")= "/ 1000"
            getIdP("len-2-formula")= "* 100"
            getIdP("len-3-formula")= "*3.28"
            getIdP("len-4-formula")= "* 1.094"
            getIdP("len-5-formula")= "/ 1809"
            getIdP("len-6-formula")= "* 39.37"

            Hide(UNIT)
        }
            

    };


};



