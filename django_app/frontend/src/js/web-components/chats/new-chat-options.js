// @ts-check

class NewChatOptions extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
        <h3 class="chat-options__heading govuk-heading-m">What would you like to ask your Redbox?</h3>
        <div class="chat-options__options">
            <button class="chat-options__option chat-options__option_topic" type="button">
                <img src="/static/icons/icon_square_question.svg" alt=""/>
                Tell me about a specific topic
            </button>
            <button class="chat-options__option chat-options__option_themes" type="button">
                <img src="/static/icons/icon_square_doc.svg" alt=""/>
                Find themes in my documents
            </button>
            <button class="chat-options__option chat-options__option_summarise" type="button">
                <img src="/static/icons/icon_pointer_dashed_square.svg" alt=""/>
                Summarise my document
            </button>
        </div>
        <p class="chat-options__info-text">Or type any question below</p>
        `;

    this.querySelector(".chat-options__option_topic")?.addEventListener(
      "click",
      (e) => {
        this.prepopulateMessageBox("Tell me about a specific topic");
      }
    );
    this.querySelector(".chat-options__option_themes")?.addEventListener(
      "click",
      (e) => {
        this.prepopulateMessageBox("Find themes in my documents");
      }
    );
    this.querySelector(".chat-options__option_summarise")?.addEventListener(
      "click",
      (e) => {
        this.prepopulateMessageBox("Summarise my document");
      }
    );

    /**
     * Ensures "Message Redbox" always aligns to the bottom (not proud of this code, but it works until I put in a better grid solution)
     */
    const setTopMargin = () => {
      this.style.marginTop = "0px";
      const offset = 47;
      const topMargin =
        document.querySelector("main").scrollHeight -
        document.querySelector(".iai-chat-input").scrollHeight -
        this.scrollHeight -
        offset;
      if (topMargin > 0) {
        this.style.marginTop = `${topMargin}px`;
      }
    };
    setTopMargin();
    window.addEventListener("resize", setTopMargin);
  }

  prepopulateMessageBox = (prompt) => {
    /** @type HTMLInputElement | null */
    let chatInput = document.querySelector(".iai-chat-input__input");
    if (chatInput) {
      chatInput.value = prompt;
      chatInput.focus();
      chatInput.selectionStart = chatInput.value.length;
    }
  };
}
customElements.define("new-chat-options", NewChatOptions);
