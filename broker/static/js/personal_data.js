const changeBtn = document.getElementById('btn-change');
const usernameInput = document.getElementById('username');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');

changeBtn.addEventListener('click', e => {
  e.preventDefault();
  console.log('sdffd')
  const data = {
    username: usernameInput.value,
    email: emailInput.value,
    password: passwordInput.value,
  }
  change(data);
});


async function change(data) {
    console.log(data)
    const response = await fetch('/personal_data', {
        method: "PUT",
        header: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
}
