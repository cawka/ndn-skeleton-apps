package examples.cs.ucla.edu.jndn;

import android.app.Activity;
import android.app.ActionBar;
import android.app.Fragment;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.os.Build;
import android.widget.TextView;

import net.named_data.jndn.Data;
import net.named_data.jndn.Face;
import net.named_data.jndn.Interest;
import net.named_data.jndn.Name;
import net.named_data.jndn.OnData;
import net.named_data.jndn.OnTimeout;


public class MainActivity extends Activity {

  @Override
  protected void onCreate(Bundle savedInstanceState)
  {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main);
    if (savedInstanceState == null) {
      getFragmentManager().beginTransaction()
        .add(R.id.container, new PlaceholderFragment())
        .commit();
    }
  }

  /**
   * A placeholder fragment containing a simple view.
   */
  public static class PlaceholderFragment extends Fragment {

    public PlaceholderFragment()
    {
    }

    @Override
    public void onCreate(Bundle savedInstanceState)
    {
      super.onCreate(savedInstanceState);
      m_handler = new Handler();
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState)
    {
      View rootView = inflater.inflate(R.layout.fragment_main, container, false);
      m_text = (TextView)rootView.findViewById(R.id.text);
      return rootView;
    }

    @Override
    public void onResume()
    {
      super.onResume();
      m_handler.post(m_runFetch);
    }

    @Override
    public void onPause()
    {
      super.onPause();
      m_handler.removeCallbacks(m_runFetch);
    }

    ///////////////////////////////////////////////////////////////////////////

    private TextView m_text;
    private Handler m_handler;

    private class FetchTask extends AsyncTask<Void, Void, String> {
      @Override
      protected String
      doInBackground(Void... voids)
      {
        try {
          m_face = new Face("localhost");
          m_face.expressInterest(new Name("/localhost/nfd"),
                                 new OnData() {
                                   @Override
                                   public void
                                   onData(Interest interest, Data data)
                                   {
                                     m_retVal = data.getContent().toString();
                                     m_shouldStop = true;
                                   }
                                 },
                                 new OnTimeout() {
                                   @Override
                                   public void onTimeout(Interest interest)
                                   {
                                     m_retVal = "ERROR: Timeout";
                                     m_shouldStop = true;
                                   }
                                 });

          while (!m_shouldStop) {
            m_face.processEvents();
            Thread.sleep(500);
          }
          m_face.shutdown();
          m_face = null;
          return m_retVal;
        }
        catch (Exception e) {
          return "ERROR: " + e.getMessage();
        }
      }

      @Override
      protected void
      onPostExecute(String result)
      {
        m_text.append(result + "\n");
      }

      private String m_retVal;
      private Face m_face;
      private boolean m_shouldStop = false;
    }

    private Runnable m_runFetch = new Runnable() {
      @Override
      public void
      run()
      {
        new FetchTask().execute();
      }
    };
  }
}
