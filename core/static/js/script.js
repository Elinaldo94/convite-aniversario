document.addEventListener("DOMContentLoaded", function () {
  // 1. MAPEAMENTO DE ELEMENTOS DO DOM
  const form = document.getElementById("formConvite");
  const radiosConfirmacao = document.querySelectorAll(
    'input[name="confirmou"]',
  );
  const blocoPresencaConfirmada = document.getElementById(
    "blocoPresencaConfirmada",
  );
  const modal = document.getElementById("modalResposta");
  const btnFecharModal = document.getElementById("btnFecharModal");

  const campoAcompanhantes =
    document.querySelector('input[name="quantidade_vinda"]') ||
    document.querySelector('select[name="quantidade_vinda"]');

  // Adiciona as classes do Bootstrap nos inputs do Django
  document
    .querySelectorAll(
      'form input[type="text"], form select, form input[type="number"]',
    )
    .forEach((el) => {
      el.classList.add("form-control");
    });

  // 2. DISPARO AUTOMÁTICO SE O DJANGO DEVOLVER SUCESSO
  const statusPopup = document.body.getAttribute("data-popup-status");
  if ((statusPopup === "confirmado" || statusPopup === "recusado") && modal) {
    modal.classList.add("mostrar");
  }

  // 3. LOGICA DE EXIBIÇÃO: SEÇÃO PRINCIPAL (SIM / NÃO)
  function gerenciarExibicaoPresenca() {
    let selecionado = document.querySelector('input[name="confirmou"]:checked');
    if (
      selecionado &&
      (selecionado.value.toLowerCase() === "sim" ||
        selecionado.value === "true" ||
        selecionado.value === "1")
    ) {
      blocoPresencaConfirmada.style.display = "block";
    } else {
      blocoPresencaConfirmada.style.display = "none";
      if (campoAcompanhantes) campoAcompanhantes.value = "";
    }
  }

  radiosConfirmacao.forEach((radio) => {
    radio.addEventListener("change", gerenciarExibicaoPresenca);
  });

  // ==========================================================================
  // 4. TRAVA DE SEGURANÇA LOCAL PARA A QUANTIDADE VINDA (BLOQUEIO DO ZERO)
  // ==========================================================================
  if (campoAcompanhantes) {
    function validarQuantidadeTempoReal() {
      let selecionado = document.querySelector(
        'input[name="confirmou"]:checked',
      );

      // A trava do zero só se aplica se o usuário marcou "Sim"
      if (
        selecionado &&
        (selecionado.value.toLowerCase() === "sim" ||
          selecionado.value === "true" ||
          selecionado.value === "1")
      ) {
        let qtd = parseInt(campoAcompanhantes.value);

        // Se o usuário digitou zero, número negativo ou esvaziou o campo temporariamente, força virar 1
        if (isNaN(qtd) || qtd < 1) {
          campoAcompanhantes.value = 1;
          return;
        }

        // Valida se ultrapassou o limite máximo vindo do banco de dados
        if (
          typeof LIMITE_CONVIDADOS !== "undefined" &&
          qtd > LIMITE_CONVIDADOS
        ) {
          alert(
            `O limite máximo de participantes para este convite é de ${LIMITE_CONVIDADOS} pessoas.`,
          );
          campoAcompanhantes.value = LIMITE_CONVIDADOS; // Força o teto máximo permitido
        }
      }
    }

    // Monitora cliques nas setinhas do campo numérico e digitação direta
    campoAcompanhantes.addEventListener("input", validarQuantidadeTempoReal);
    campoAcompanhantes.addEventListener("change", validarQuantidadeTempoReal);

    // Garante que o campo nunca fique totalmente vazio caso o usuário apague tudo e clique fora dele
    campoAcompanhantes.addEventListener("blur", function () {
      let selecionado = document.querySelector(
        'input[name="confirmou"]:checked',
      );
      if (
        selecionado &&
        (selecionado.value.toLowerCase() === "sim" ||
          selecionado.value === "true" ||
          selecionado.value === "1")
      ) {
        if (
          !campoAcompanhantes.value ||
          parseInt(campoAcompanhantes.value) < 1
        ) {
          campoAcompanhantes.value = 1;
        }
      }
    });
  }

  // 5. CONTROLE DO MODAL DE FEEDBACK (FECHAMENTO)
  if (btnFecharModal && modal) {
    btnFecharModal.addEventListener("click", function () {
      modal.classList.remove("mostrar");
    });
  }

  // 6. EXECUÇÕES INICIAIS PREVENTIVAS
  if (!statusPopup) {
    gerenciarExibicaoPresenca();
  } else {
    if (statusPopup === "confirmado") {
      blocoPresencaConfirmada.style.display = "block";
    } else {
      blocoPresencaConfirmada.style.display = "none";
    }
  }
});
