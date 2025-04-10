using UnityEngine;
using UnityEngine.SceneManagement;


public class MainMenuController : MonoBehaviour
{
    public GameObject quitConfirmationPanel; // ����Ԥ�贰��

    public void StartGame()
    {
        Debug.Log("Start Game");
        // ������Ϊ GameScene �ĳ���
        SceneManager.LoadScene("GameScene");
    }


    public void OpenOptions()
    {
        Debug.Log("Open Options");
    }

    public void QuitGame()
    {
        // ��ʾȷ���˳�����
        quitConfirmationPanel.SetActive(true);
    }

    public void ConfirmQuit()
    {
        Debug.Log("Quit Confirmed");
        Application.Quit();
    }

    public void CancelQuit()
    {
        // �����˳�����
        quitConfirmationPanel.SetActive(false);
    }
}
