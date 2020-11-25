<script>

	let messages = [];
	let name = "";
	let inputText = "";
	let inputName = "";
	let inputPrivateText = "";
	let backtext = "Digite seu nome";
	let n_users = "";

	const ws = new WebSocket("ws://localhost:8765");

	ws.onopen = function(){
		inputText = ""
	};
	ws.onmessage = function(e){
		let data = JSON.parse(e.data);
		let msg = "";
		if(data.type == "message"){
			msg = data.user + ": " + data.message;
			messages = [...messages, msg];
		}else if(data.type == "users"){
			n_users = data.count + " user(s) conectado(s)";
		}else if(data.type == "name"){
			name = data.name;
			backtext = "Digite sua mensagem";
		}

	};
	function handleClick(){
		ws.send(JSON.stringify({type:"message", message:inputText, user:name}));
		messages = [...messages, "Enviado: "+inputText];
		inputText = "";
	}
	function handlePrivateClick(){
		if (name != ""){
			ws.send(JSON.stringify({type:"private", message:inputPrivateText, user:name, to:inputName}));
			messages = [...messages, "Enviado para "+ inputName+ " : " + inputText];
		}
		inputPrivateText = "";
		inputName = "";
	}

</script>

<main>

	<h1>Poli Chat</h1>

	<h3>Chat:</h3>

		<div class="my_box">
			{#each messages as message}
			<p style="text-align: left"> {message} </p>
			{/each}
		</div>

		<div style="padding: 5px 0">
				<input type="text" bind:value={inputText} placeholder={backtext}/>
				<button on:click={handleClick}>Enviar</button>
		</div>
		<h3>Mensagens privadas</h3>
		<div style="border: 1px solid Black; padding: 5px 0" >
			Nome:
			<input type="text" bind:value={inputName} placeholder="Nome do usuário"/>
			Mensagem
			<input type="text" bind:value={inputPrivateText} placeholder="Digite sua mensagem"/>
			<button on:click={handlePrivateClick}>Enviar privado</button>
		</div>
		<div>
			{n_users}
		</div>

</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}
	.my_box{
		height:180px;
		width:500px;
		border:1px solid #ff3e00;
		overflow:auto;
		background-color:white;
		color:black;
		scrollbar-base-color:gold;
		font-family:sans-serif;
		padding:5px;
		margin: auto;
	}

	h1 {
		color: #ff3e00;
		font-size: 3em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
