<div class="scroller">
    <table class="data-table cell-border compact hover stripe">
      <thead>
        <tr>
          % for head in table['heads']:
            <th>{{head}}</th>
          % end
        </tr>
      </thead>
      <tbody>
      % for row in table['rows']:
        <tr>
        % for key, value in row.iteritems():
          <td>{{value}}</td>
        % end
        </tr>
      % end
      </tbody>
    </table>
  </div>
  
  <div>
  
  </div>