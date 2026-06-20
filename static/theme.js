const toggle =
document.getElementById(
"themeToggle"
);

if(
localStorage.getItem(
"theme"
) === "light"
){

document.body.classList.add(
"light-mode"
);

}

toggle.addEventListener(
"click",
()=>{

document.body.classList.toggle(
"light-mode"
);

if(
document.body.classList.contains(
"light-mode"
)
){

localStorage.setItem(
"theme",
"light"
);

toggle.innerHTML =
"🌙 Dark Mode";

}
else{

localStorage.setItem(
"theme",
"dark"
);

toggle.innerHTML =
"☀️ Light Mode";

}

});