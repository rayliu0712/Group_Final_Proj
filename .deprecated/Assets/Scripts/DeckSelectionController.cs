using UnityEngine;
using UnityEngine.SceneManagement;

public class DeckSelectionController : MonoBehaviour
{
    public void OnWarriorButtonClicked()
    {
        DeckSelectionData.SelectedDeck = "Warrior";
        SceneManager.LoadScene("DeckPreviewScene");
    }

    public void OnArcherButtonClicked()
    {
        DeckSelectionData.SelectedDeck = "Archer";
        SceneManager.LoadScene("DeckPreviewScene");
    }

    public void OnAssassinButtonClicked()
    {
        DeckSelectionData.SelectedDeck = "Assassin";
        SceneManager.LoadScene("DeckPreviewScene");
    }
}
