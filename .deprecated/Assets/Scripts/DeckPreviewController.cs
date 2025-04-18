using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;
using System.Collections.Generic;

public class DeckPreviewController : MonoBehaviour
{
    public Text deckTitle;
    public Transform cardContainer;
    public GameObject cardPrefab;
    public Button confirmButton;
    public Button backButton;

    private string selectedDeck;

    void Start()
    {
        selectedDeck = PlayerPrefs.GetString("SelectedDeck");
        deckTitle.text = selectedDeck + " Deck";
        DisplayCardsForDeck(selectedDeck);

        confirmButton.onClick.AddListener(OnConfirm);
        backButton.onClick.AddListener(OnBack);
    }

    void DisplayCardsForDeck(string deck)
    {
        List<string> cardNames = new List<string>();

        switch (deck)
        {
            case "Warrior":
                cardNames.AddRange(GenerateCards("Attack", 5));
                cardNames.AddRange(GenerateCards("Defense", 5));
                cardNames.AddRange(GenerateCards("Skill", 2));
                break;
            case "Archer":
                cardNames.AddRange(GenerateCards("Arrow", 5));
                cardNames.AddRange(GenerateCards("Dodge", 5));
                cardNames.AddRange(GenerateCards("Focus", 2));
                break;
            case "Assassin":
                cardNames.AddRange(GenerateCards("Strike", 5));
                cardNames.AddRange(GenerateCards("Shadow", 5));
                cardNames.AddRange(GenerateCards("Poison", 2));
                break;
        }

        foreach (string cardName in cardNames)
        {
            GameObject card = Instantiate(cardPrefab, cardContainer);
            card.GetComponentInChildren<Text>().text = cardName;
        }
    }

    List<string> GenerateCards(string type, int count)
    {
        List<string> cards = new List<string>();
        for (int i = 1; i <= count; i++)
        {
            cards.Add(type + " Card " + i);
        }
        return cards;
    }

    void OnConfirm()
    {
        Debug.Log("Confirmed deck: " + selectedDeck);
        SceneManager.LoadScene("GameScene");
    }

    void OnBack()
    {
        SceneManager.LoadScene("DeckSelectionScene");
    }
}
