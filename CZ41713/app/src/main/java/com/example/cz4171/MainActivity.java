package com.example.cz4171;

import android.os.Bundle;
import com.google.android.material.snackbar.Snackbar;
import androidx.appcompat.app.AppCompatActivity;
import android.view.View;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;
import com.example.cz4171.databinding.ActivityMainBinding;
import android.view.Menu;
import android.view.MenuItem;
import android.os.Bundle;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import org.jetbrains.annotations.NotNull;
import java.io.IOException;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import java.io.IOException;
import java.util.concurrent.TimeUnit;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {

    private EditText textField_message;
    private Button button_send_post;
    private Button button_send_update;
    private Button button_send_get;
    private TextView textView_response;
    private String url="http://192.168.1.5:5000/";
    private String POST="POST";
    private String GET="GET";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textField_message=findViewById(R.id.txtField_message);
        button_send_post=findViewById(R.id.button_send_post);
        button_send_update=findViewById(R.id.button_send_update);
        button_send_get=findViewById(R.id.button_send_get);
        textView_response=findViewById(R.id.textView_response);

        button_send_get.setOnClickListener(view -> {
            sendRequest(GET,"get",null,null);
        });

        button_send_post.setOnClickListener(view -> {
            String text=textField_message.getText().toString();
            if(text.isEmpty()){
                textField_message.setError("This cannot be empty for post request");
            }else {
                sendRequest(POST, "getresult", "sms", text);
            }
        });

        button_send_update.setOnClickListener(view -> {
            String text=textField_message.getText().toString();
            if(text.isEmpty()){
                textField_message.setError("This cannot be empty for post request");
            }else {
                sendRequest(POST, "updatemodel", "sms", text);
            }
        });
    }

void sendRequest(String type,String method,String paramname,String param){

    String fullURL=url+"/"+method+(param==null?"":"/"+param);
    Request request;

    OkHttpClient client = new OkHttpClient().newBuilder()
            .connectTimeout(10, TimeUnit.SECONDS)
            .readTimeout(10, TimeUnit.SECONDS)
            .writeTimeout(10, TimeUnit.SECONDS).build();

    if(type.equals(POST)){
        RequestBody formBody = new FormBody.Builder().add(paramname, param).build();
        request=new Request.Builder().url(fullURL).post(formBody).build();
    }else{
        request = new Request.Builder().url(fullURL).build();
    }

    client.newCall(request).enqueue(new Callback() {
        @Override
        public void onFailure(@NonNull Call call, @NonNull IOException e) {
            e.printStackTrace();
        }

        @Override
        public void onResponse(Call call, final Response response) throws IOException {
            final String responseData = response.body().string();
            MainActivity.this.runOnUiThread(() -> textView_response.setText(responseData));
        }
    });
}
}