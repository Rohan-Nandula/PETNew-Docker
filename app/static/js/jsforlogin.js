const RegisterButton = document.getElementById('Register');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

RegisterButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});