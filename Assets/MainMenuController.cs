using UnityEngine;
using UnityEngine.SceneManagement;

public class MainMenuController : MonoBehaviour
{
    public GameObject quitConfirmationPanel; // 拖入预设窗口

    public void StartGame()
    {
        Debug.Log("Start Game");
        // 改为加载卡组选择场景（DeckSelectionScene）
        SceneManager.LoadScene("DeckSelectionScene");
    }

    public void OpenOptions()
    {
        Debug.Log("Open Options");
    }

    public void QuitGame()
    {
        // 显示确认退出窗口
        quitConfirmationPanel.SetActive(true);
    }

    public void ConfirmQuit()
    {
        Debug.Log("Quit Confirmed");
        Application.Quit();
    }

    public void CancelQuit()
    {
        // 隐藏退出窗口
        quitConfirmationPanel.SetActive(false);
    }
}
