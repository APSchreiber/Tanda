 <div class="scroller">
  <table class="data-table cell-border compact hover stripe">
    <thead>
      <tr>
        % heads = list(items[0])
        % for head in heads:
          <th>{{head}}</th>
        % end
      </tr>
    </thead>
    <tbody>
    % for item in items:
      <tr>
      % for key, value in item.iteritems():
        <td>{{value}}</td>
      % end
      </tr>
    % end
    </tbody>
  </table>
</div>

<div>

</div>